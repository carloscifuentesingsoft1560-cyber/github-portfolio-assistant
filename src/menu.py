from src.git_manager import GitManager
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
                self._opcion_no_disponible("Crear proyecto")

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
                print("\nOpción no válida. Seleccione un número entre 1 y 7.")

    @staticmethod
    def _mostrar_menu() -> None:
        print("\n" + "=" * 60)
        print("           GITHUB PORTFOLIO ASSISTANT")
        print("=" * 60)
        print("1. Crear proyecto")
        print("2. Consultar estado Git")
        print("3. Agregar cambios (git add .)")
        print("4. Analizar proyecto")
        print("5. Revisar seguridad")
        print("6. Configuración")
        print("7. Salir")
        print("=" * 60)

    def _consultar_estado_git(self) -> None:
        ruta = input("\nRuta del proyecto: ").strip()

        try:
            proyecto = self.project_manager.load_project(ruta)

            if not proyecto.is_git_repository:
                print("\nLa carpeta seleccionada no es un repositorio Git.")
                return

            git_manager = GitManager(proyecto)
            resultado = git_manager.status()

            if resultado.success:
                print("\nEstado del repositorio:\n")
                print(resultado.output)
            else:
                print("\nNo fue posible consultar el estado del repositorio.")
                print(resultado.error)

        except (FileNotFoundError, NotADirectoryError) as error:
            print(f"\nError: {error}")

    def _agregar_cambios(self) -> None:
        ruta = input("\nRuta del proyecto: ").strip()

        try:
            proyecto = self.project_manager.load_project(ruta)

            if not proyecto.is_git_repository:
                print("\nLa carpeta seleccionada no es un repositorio Git.")
                return

            git_manager = GitManager(proyecto)
            resultado = git_manager.add_all()

            if resultado.success:
                print("\n✅ Cambios agregados correctamente al área de preparación (git add .).")
            else:
                print("\n❌ No fue posible agregar los cambios.")
                print(resultado.error)

        except (FileNotFoundError, NotADirectoryError) as error:
            print(f"\nError: {error}")

    @staticmethod
    def _opcion_no_disponible(nombre: str) -> None:
        print(f"\nLa opción '{nombre}' estará disponible en un próximo sprint.")