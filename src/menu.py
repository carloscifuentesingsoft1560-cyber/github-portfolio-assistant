from src.git_manager import GitManager
from src.github_manager import GitHubManager
from src.project_manager import ProjectManager


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
                self._opcion_no_disponible("Analizar proyecto")

            elif opcion == "5":
                self._opcion_no_disponible("Revisar seguridad")

            elif opcion == "6":
                self._opcion_no_disponible("Configuración")

            elif opcion == "7":
                print("\nHasta luego.")
                break

            else:
                print(
                    "\nOpción no válida. "
                    "Seleccione un número entre 1 y 7."
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
        print("5. Revisar seguridad")
        print("6. Configuración")
        print("7. Salir")
        print("=" * 60)

    def _publicar_proyecto_existente(self) -> None:
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

            print(
                "Cambios agregados correctamente."
            )

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
                print(
                    "Commit creado correctamente."
                )

                if commit_result.output:
                    print(commit_result.output)

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

    @staticmethod
    def _opcion_no_disponible(
        nombre: str,
    ) -> None:
        print(
            f"\nLa opción '{nombre}' "
            "estará disponible próximamente."
        )