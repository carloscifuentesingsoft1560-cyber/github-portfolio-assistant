from src.git_manager import GitManager
from src.github_manager import GitHubManager
from src.project_analyzer import ProjectAnalyzer
from src.project_manager import ProjectManager
from src.readme_generator import ReadmeGenerator
from src.security_checker import SecurityChecker
from src.commit_generator import CommitGenerator
from src.config import AppConfig

class Menu:
    """
    Administra el menú principal de la aplicación.
    """

    def __init__(self) -> None:
        self.project_manager = ProjectManager()
        self.config = AppConfig()

    def iniciar(self) -> None:
        while True:
            self._mostrar_menu()

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._publicar_proyecto_existente()

            elif opcion == "2":
                self._consultar_estado_git()

            elif opcion == "3":
                self._agregar_cambios()

            elif opcion == "4":
                self._analizar_proyecto()

            elif opcion == "5":
                self._generar_readme()

            elif opcion == "6":
                self._revisar_seguridad()

            elif opcion == "7":
                self._configuracion()

            elif opcion == "8":
                print("\nHasta luego.")
                break

            else:
                print(
                    "\nOpción no válida. "
                    "Seleccione un número entre 1 y 8."
                )

    @staticmethod
    def _mostrar_menu() -> None:
        print("\n" + "=" * 60)
        print("           GITHUB PORTFOLIO ASSISTANT")
        print("=" * 60)
        print("1. Publicar proyecto existente")
        print("2. Consultar estado Git")
        print("3. Agregar cambios (git add .)")
        print("4. Analizar proyecto")
        print("5. Generar README")
        print("6. Revisar seguridad")
        print("7. Configuración")
        print("8. Salir")
        print("=" * 60)

    def _publicar_proyecto_existente(self) -> None:
        """
        Publica un proyecto existente en GitHub.
        """

        ruta = input(
            "\nRuta del proyecto que desea publicar: "
        ).strip()

        try:
            proyecto = self.project_manager.load_project(ruta)

            if not proyecto.is_git_repository:
                print(
                    "\nLa carpeta seleccionada no es "
                    "un repositorio Git."
                )
                return

            git = GitManager(proyecto)
            github = GitHubManager(proyecto)

            # --------------------------------------------------
            # Comprobar autenticación en GitHub
            # --------------------------------------------------

            print("\n--- Comprobar GitHub ---")

            auth_result = github.auth_status()

            if not auth_result.success:
                print(
                    "\nNo fue posible autenticar GitHub CLI."
                )

                if auth_result.error:
                    print(auth_result.error)

                return

            print("GitHub CLI autenticado correctamente.")

            # --------------------------------------------------
            # Consultar estado del proyecto
            # --------------------------------------------------

            print("\n--- Estado del proyecto ---")

            status_result = git.status()

            if status_result.success:
                print(status_result.output)

            else:
                print(
                    "\nNo fue posible consultar "
                    "el estado del repositorio."
                )

                if status_result.error:
                    print(status_result.error)

                return

            # --------------------------------------------------
            # Revisar origin
            # --------------------------------------------------

            print("\n--- Revisar remoto origin ---")

            origin_result = git.get_remote_origin()

            if origin_result.success:
                print(
                    "Origin configurado:",
                    origin_result.output,
                )

                confirmacion = input(
                    "\n¿Desea publicar en este origin? "
                    "(s/n): "
                ).strip().lower()

                if confirmacion != "s":
                    print("\nOperación cancelada.")
                    return

            else:
                print(
                    "El proyecto no tiene origin configurado."
                )

                repository_name = input(
                    "Nombre del repositorio en GitHub: "
                ).strip()

                if not repository_name:
                    print(
                        "\nEl nombre del repositorio "
                        "no puede estar vacío."
                    )
                    return

                visibility = input(
                    "Visibilidad (public/private) "
                    "[public]: "
                ).strip().lower()

                if not visibility:
                    visibility = "public"

                confirmation = input(
                    f"\n¿Crear '{repository_name}' "
                    f"como repositorio {visibility}? "
                    "(s/n): "
                ).strip().lower()

                if confirmation != "s":
                    print("\nOperación cancelada.")
                    return

                create_result = github.create_repository(
                    repository_name=repository_name,
                    visibility=visibility,
                )

                if not create_result.success:
                    print(
                        "\nNo fue posible crear "
                        "el repositorio."
                    )

                    if create_result.error:
                        print(create_result.error)

                    return

                print(
                    "\nRepositorio creado correctamente."
                )

                if create_result.output:
                    print(create_result.output)
            
            # --------------------------------------------------
            # Revisión de seguridad
            # --------------------------------------------------

            print("\n--- Revisión de seguridad ---")

            security_checker = SecurityChecker(proyecto)
            security_result = security_checker.check()

            if security_result["safe"]:
                print(
                    "No se encontraron archivos "
                    "problemáticos sin protección."
                )

            else:
                print(
                    "\nADVERTENCIA: se encontraron archivos "
                    "que requieren revisión."
                )

                print("\nArchivos no protegidos:")

                for item in security_result["unprotected_files"]:
                    categorias = ", ".join(
                        item["categories"]
                    )

                    print(
                        f"- {item['path']} "
                        f"[{categorias}] "
                        f"({item['size_mb']} MB)"
                    )

                print("\nAdvertencias:")

                for warning in security_result["warnings"]:
                    print(f"- {warning}")

                continuar = input(
                    "\n¿Desea continuar con la publicación "
                    "de todos modos? (s/n): "
                ).strip().lower()

                if continuar != "s":
                    print(
                        "\nPublicación cancelada por seguridad."
                    )
                    return
            # --------------------------------------------------
            # Agregar cambios
            # --------------------------------------------------

            print("\n--- Preparar cambios ---")

            add_result = git.add_all()

            if not add_result.success:
                print(
                    "\nNo fue posible agregar "
                    "los cambios."
                )

                if add_result.error:
                    print(add_result.error)

                return

            print("Cambios agregados correctamente.")

            # --------------------------------------------------
            # Comprobar si existen cambios para commit
            # --------------------------------------------------

            pending_result = git.execute(
                ["status", "--short"]
            )

            if not pending_result.success:
                print(
                    "\nNo fue posible comprobar "
                    "los cambios pendientes."
                )

                if pending_result.error:
                    print(pending_result.error)

                return

            if not pending_result.output.strip():
                print(
                    "\nNo hay cambios nuevos "
                    "para crear un commit."
                )

                print(
                    "Se continuará con la comprobación "
                    "de publicación en GitHub."
                )

            else:
                # ----------------------------------------------
                # Generar mensaje de commit sugerido
                # ----------------------------------------------

                commit_generator = CommitGenerator(
                    proyecto
                )

                mensaje_sugerido = (
                    commit_generator.generate()
                )

                print(
                    "\nMensaje de commit sugerido:"
                )
                print(mensaje_sugerido)

                mensaje = input(
                    "\nPresione Enter para usarlo "
                    "o escriba otro mensaje: "
                ).strip()

                if not mensaje:
                    mensaje = mensaje_sugerido

                print(
                    f"\nMensaje seleccionado: "
                    f"{mensaje}"
                )

                # ----------------------------------------------
                # Crear commit
                # ----------------------------------------------

                print("\n--- Crear commit ---")

                commit_result = git.commit(
                    mensaje
                )

                if not commit_result.success:
                    error = (
                        commit_result.error
                        or commit_result.output
                        or ""
                    )

                    print(
                        "\nNo fue posible crear "
                        "el commit."
                    )

                    if error:
                        print(error)

                    return

                print(
                    "Commit creado correctamente."
                )

                if commit_result.output:
                    print(commit_result.output)
            # --------------------------------------------------
            # Push
            # --------------------------------------------------

            print("\n--- Publicar en GitHub ---")

            push_result = git.push()

            if push_result.success:
                print(
                    "\nProyecto publicado "
                    "correctamente en GitHub."
                )

                if push_result.output:
                    print(push_result.output)

            else:
                print(
                    "\nNo fue posible publicar "
                    "el proyecto."
                )

                if push_result.error:
                    print(push_result.error)

        except (
            FileNotFoundError,
            NotADirectoryError,
        ) as error:
            print(f"\nError: {error}")

    def _consultar_estado_git(self) -> None:
        """
        Consulta el estado Git de un proyecto.
        """

        ruta = input("\nRuta del proyecto: ").strip()

        try:
            proyecto = self.project_manager.load_project(
                ruta
            )

            if not proyecto.is_git_repository:
                print(
                    "\nLa carpeta seleccionada no es "
                    "un repositorio Git."
                )
                return

            git_manager = GitManager(proyecto)

            resultado = git_manager.status()

            if resultado.success:
                print("\nEstado del repositorio:\n")
                print(resultado.output)

            else:
                print(
                    "\nNo fue posible consultar "
                    "el estado del repositorio."
                )

                if resultado.error:
                    print(resultado.error)

        except (
            FileNotFoundError,
            NotADirectoryError,
        ) as error:
            print(f"\nError: {error}")

    def _agregar_cambios(self) -> None:
        """
        Ejecuta git add . sobre el proyecto.
        """

        ruta = input("\nRuta del proyecto: ").strip()

        try:
            proyecto = self.project_manager.load_project(
                ruta
            )

            if not proyecto.is_git_repository:
                print(
                    "\nLa carpeta seleccionada no es "
                    "un repositorio Git."
                )
                return

            git_manager = GitManager(proyecto)

            resultado = git_manager.add_all()

            if resultado.success:
                print(
                    "\nCambios agregados correctamente "
                    "al área de preparación."
                )

            else:
                print(
                    "\nNo fue posible agregar "
                    "los cambios."
                )

                if resultado.error:
                    print(resultado.error)

        except (
            FileNotFoundError,
            NotADirectoryError,
        ) as error:
            print(f"\nError: {error}")

    def _analizar_proyecto(self) -> None:
        """
        Analiza la estructura general de un proyecto.
        """

        ruta = input("\nRuta del proyecto: ").strip()

        try:
            proyecto = self.project_manager.load_project(
                ruta
            )

            analyzer = ProjectAnalyzer(proyecto)

            resultado = analyzer.analyze()
          
            print("\n" + "=" * 60)
            print("              ANÁLISIS DEL PROYECTO")
            print("=" * 60)

            print(
                f"Nombre: {resultado['name']}"
            )

            print(
                f"Ruta: {resultado['path']}"
            )

            print(
                "Repositorio Git:",
                "Sí"
                if resultado["is_git_repository"]
                else "No",
            )

            print(
                "README:",
                "Sí"
                if resultado["has_readme"]
                else "No",
            )

            print(
                ".gitignore:",
                "Sí"
                if resultado["has_gitignore"]
                else "No",
            )

            print(
                "requirements.txt:",
                "Sí"
                if resultado["has_requirements"]
                else "No",
            )

            print(
                f"Archivos: "
                f"{resultado['file_count']}"
            )

            print(
                f"Carpetas: "
                f"{resultado['directory_count']}"
            )

            tecnologias = resultado["technologies"]

            print(
                "Tecnologías:",
                ", ".join(tecnologias)
                if tecnologias
                else "No detectadas",
            )

            print("=" * 60)

        except (
            FileNotFoundError,
            NotADirectoryError,
        ) as error:
            print(f"\nError: {error}")

    def _generar_readme(self) -> None:
        """
        Genera un README.md para un proyecto.
        """

        ruta = input(
            "\nRuta del proyecto: "
        ).strip()

        try:
            proyecto = self.project_manager.load_project(ruta)

            generator = ReadmeGenerator(proyecto)

            print("\n" + "=" * 60)
            print("              VISTA PREVIA DEL README")
            print("=" * 60)

            contenido = generator.generate_content()

            print()
            print(contenido)
            print("=" * 60)

            readme_path = proyecto.path / "README.md"

            if readme_path.exists():
                print(
                    "\nEl proyecto ya contiene un README.md."
                )

                respuesta = input(
                    "¿Desea reemplazarlo? (s/n): "
                ).strip().lower()

                if respuesta != "s":
                    print(
                        "\nREADME conservado. "
                        "No se realizó ningún cambio."
                    )
                    return

                generator.write(
                    overwrite=True
                )

                print(
                    "\nREADME.md reemplazado correctamente."
                )

            else:
                respuesta = input(
                    "\n¿Desea crear este README.md? (s/n): "
                ).strip().lower()

                if respuesta != "s":
                    print("\nOperación cancelada.")
                    return

                generator.write()

                print(
                    "\nREADME.md creado correctamente."
                )

        except (
            FileNotFoundError,
            NotADirectoryError,
        ) as error:
            print(f"\nError: {error}")

        except FileExistsError as error:
            print(f"\nError: {error}")

    def _revisar_seguridad(self) -> None:
        """
        Revisa posibles riesgos antes de publicar un proyecto.
        """

        ruta = input(
            "\nRuta del proyecto: "
        ).strip()

        try:
            proyecto = self.project_manager.load_project(
                ruta
            )

            checker = SecurityChecker(proyecto)

            resultado = checker.check()

            print("\n" + "=" * 60)
            print("              REVISIÓN DE SEGURIDAD")
            print("=" * 60)

            print(
                "Estado:",
                "SEGURO"
                if resultado["safe"]
                else "REQUIERE REVISIÓN",
            )

            print(
                "\n--- Archivos potencialmente problemáticos ---"
            )

            if resultado["detected_files"]:
                for item in resultado["detected_files"]:
                    categorias = ", ".join(
                        item["categories"]
                    )

                    print(
                        f"- {item['path']} "
                        f"[{categorias}] "
                        f"({item['size_mb']} MB)"
                    )
            else:
                print("Ninguno.")

            print("\n--- Protegidos por .gitignore ---")

            if resultado["protected_files"]:
                for item in resultado["protected_files"]:
                    print(f"- {item['path']}")
            else:
                print("Ninguno.")

            print("\n--- No protegidos ---")

            if resultado["unprotected_files"]:
                for item in resultado["unprotected_files"]:
                    print(f"- {item['path']}")
            else:
                print("Ninguno.")

            print("\n--- Advertencias ---")

            if resultado["warnings"]:
                for warning in resultado["warnings"]:
                    print(f"- {warning}")
            else:
                print(
                    "No se encontraron advertencias."
                )

            print("=" * 60)

        except (
            FileNotFoundError,
            NotADirectoryError,
        ) as error:
            print(f"\nError: {error}")

    def _configuracion(self) -> None:
        """
        Permite consultar y modificar la configuración
        general de la aplicación.
        """

        while True:
            settings = self.config.load()

            print("\n" + "=" * 60)
            print("                 CONFIGURACIÓN")
            print("=" * 60)

            print(
                f"1. Autor por defecto: "
                f"{settings['author'] or 'No definido'}"
            )

            print(
                f"2. Visibilidad por defecto: "
                f"{settings['default_visibility']}"
            )

            print(
                f"3. Prefijo de commit por defecto: "
                f"{settings['default_commit_prefix']}"
            )

            print(
                f"4. Confirmar antes de push: "
                f"{'Sí' if settings['confirm_before_push'] else 'No'}"
            )

            print("5. Volver")
            print("=" * 60)

            opcion = input(
                "Seleccione una opción: "
            ).strip()

            if opcion == "1":
                author = input(
                    "\nNuevo autor: "
                ).strip()

                self.config.update(
                    "author",
                    author,
                )

                print(
                    "\nAutor actualizado correctamente."
                )

            elif opcion == "2":
                visibility = input(
                    "\nVisibilidad "
                    "(public/private): "
                ).strip().lower()

                if visibility not in {
                    "public",
                    "private",
                }:
                    print(
                        "\nValor no válido."
                    )
                    continue

                self.config.update(
                    "default_visibility",
                    visibility,
                )

                print(
                    "\nVisibilidad actualizada."
                )

            elif opcion == "3":
                prefix = input(
                    "\nPrefijo de commit "
                    "(feat/fix/docs/test/chore): "
                ).strip().lower()

                valid_prefixes = {
                    "feat",
                    "fix",
                    "docs",
                    "test",
                    "chore",
                }

                if prefix not in valid_prefixes:
                    print(
                        "\nPrefijo no válido."
                    )
                    continue

                self.config.update(
                    "default_commit_prefix",
                    prefix,
                )

                print(
                    "\nPrefijo actualizado."
                )

            elif opcion == "4":
                current_value = settings[
                    "confirm_before_push"
                ]

                self.config.update(
                    "confirm_before_push",
                    not current_value,
                )

                print(
                    "\nConfirmación antes de push "
                    "actualizada."
                )

            elif opcion == "5":
                break

            else:
                print(
                    "\nOpción no válida. "
                    "Seleccione un número entre 1 y 5."
                )

    @staticmethod
    def _opcion_no_disponible(
        nombre: str,
    ) -> None:
        """
        Muestra un mensaje para funciones
        todavía no implementadas.
        """

        print(
            f"\nLa opción '{nombre}' "
            "estará disponible próximamente."
        )