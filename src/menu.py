from src.git_manager import GitManager
from src.github_manager import GitHubManager
from src.project_analyzer import ProjectAnalyzer
from src.project_manager import ProjectManager
from src.readme_generator import ReadmeGenerator


class Menu:
    """
    Administra el menú principal de la aplicación.
    """

    def __init__(self) -> None:
        self.project_manager = ProjectManager()

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
                self._opcion_no_disponible("Revisar seguridad")

            elif opcion == "7":
                self._opcion_no_disponible("Configuración")

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
            # Crear commit
            # --------------------------------------------------

            mensaje = input(
                "\nMensaje del commit: "
            ).strip()

            if not mensaje:
                print(
                    "\nEl mensaje del commit "
                    "no puede estar vacío."
                )
                return

            print("\n--- Crear commit ---")

            commit_result = git.commit(mensaje)

            if not commit_result.success:
                error = (
                    commit_result.error
                    or commit_result.output
                    or ""
                )

                if (
                    "nothing to commit" in error.lower()
                    or "nothing added to commit"
                    in error.lower()
                ):
                    print(
                        "No hay cambios nuevos "
                        "para crear un commit."
                    )

                else:
                    print(
                        "\nNo fue posible "
                        "crear el commit."
                    )

                    if error:
                        print(error)

                    return

            else:
                print("Commit creado correctamente.")

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