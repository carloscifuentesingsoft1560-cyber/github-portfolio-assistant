class Menu:
    """Administra el menú principal de la aplicación."""

    def iniciar(self) -> None:
        while True:
            self._mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._opcion_no_disponible("Crear proyecto")
            elif opcion == "2":
                self._opcion_no_disponible("Publicar proyecto existente")
            elif opcion == "3":
                self._opcion_no_disponible("Generar README")
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
        print("2. Publicar proyecto existente")
        print("3. Generar README")
        print("4. Analizar proyecto")
        print("5. Revisar seguridad")
        print("6. Configuración")
        print("7. Salir")
        print("=" * 60)

    @staticmethod
    def _opcion_no_disponible(nombre: str) -> None:
        print(f"\nLa opción '{nombre}' estará disponible próximamente.")