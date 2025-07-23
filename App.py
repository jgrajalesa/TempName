import datetime

class Transaccion:
    def __init__(self, tipo, descripcion, monto):
        self.tipo = tipo  # "ingreso" o "gasto"
        self.descripcion = descripcion
        self.monto = monto
        self.fecha = datetime.datetime.now()

    def __str__(self):
        signo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.fecha.strftime('%Y-%m-%d %H:%M')}] {self.descripcion}: {signo}${abs(self.monto):,.2f}"

class FinanzasPersonales:
    def __init__(self):
        self.transacciones = []

    def agregar_transaccion(self, tipo):
        descripcion = input("Descripción: ")
        monto = float(input("Monto: "))
        if tipo == "gasto":
            monto = -abs(monto)
        else:
            monto = abs(monto)
        self.transacciones.append(Transaccion(tipo, descripcion, monto))
        print("✅ Transacción agregada.")

    def mostrar_balance(self):
        balance = sum(t.monto for t in self.transacciones)
        print(f"\n💰 Balance actual: ${balance:,.2f}\n")

    def listar_transacciones(self):
        if not self.transacciones:
            print("No hay transacciones registradas.")
        else:
            print("\n📜 Historial de transacciones:")
            for i, t in enumerate(self.transacciones):
                print(f"{i + 1}. {t}")
            print()

    def eliminar_transaccion(self):
        self.listar_transacciones()
        idx = int(input("Número de transacción a eliminar: ")) - 1
        if 0 <= idx < len(self.transacciones):
            self.transacciones.pop(idx)
            print("🗑️ Transacción eliminada.")
        else:
            print("❌ Índice inválido.")

    def editar_transaccion(self):
        self.listar_transacciones()
        idx = int(input("Número de transacción a editar: ")) - 1
        if 0 <= idx < len(self.transacciones):
            t = self.transacciones[idx]
            print(f"Editando: {t}")
            nueva_desc = input(f"Nueva descripción (actual: {t.descripcion}): ") or t.descripcion
            nuevo_monto = input(f"Nuevo monto (actual: {abs(t.monto)}): ")
            if nuevo_monto:
                nuevo_monto = float(nuevo_monto)
                if t.monto < 0:
                    nuevo_monto = -abs(nuevo_monto)
                else:
                    nuevo_monto = abs(nuevo_monto)
            else:
                nuevo_monto = t.monto
            self.transacciones[idx] = Transaccion(t.tipo, nueva_desc, nuevo_monto)
            print("✏️ Transacción modificada.")
        else:
            print("❌ Índice inválido.")

def menu():
    app = FinanzasPersonales()
    while True:
        print("\n=== GESTOR DE FINANZAS PERSONALES ===")
        print("1. Agregar ingreso")
        print("2. Agregar gasto")
        print("3. Ver balance")
        print("4. Listar transacciones")
        print("5. Eliminar transacción")
        print("6. Editar transacción")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            app.agregar_transaccion("ingreso")
        elif opcion == "2":
            app.agregar_transaccion("gasto")
        elif opcion == "3":
            app.mostrar_balance()
        elif opcion == "4":
            app.listar_transacciones()
        elif opcion == "5":
            app.eliminar_transaccion()
        elif opcion == "6":
            app.editar_transaccion()
        elif opcion == "0":
            print("👋 Saliendo del gestor. ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    menu()