import pprint
from pymongo import MongoClient
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from bson import ObjectId
import pymongo

# Configuración de la consola de Rich
console = Console()

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["blog_db"]


def main_menu():
    console.print("\n[bold green]Bienvenido al Administrador de Base de Datos[/bold green]", justify="center")
    console.print("[cyan]Selecciona una acción:[/cyan]", justify="center")
    console.print("[1] Crear documento")
    console.print("[2] Leer documentos")
    console.print("[3] Actualizar documento")
    console.print("[4] Eliminar documento")
    console.print("[5] Salir")

    choice = Prompt.ask("[bold yellow]Opción[/bold yellow]")
    return choice


def select_collection():
    console.print("\n[bold cyan]Selecciona la colección[/bold cyan]:")
    console.print("[1] users")
    console.print("[2] articles")
    console.print("[3] comments")
    console.print("[4] tags")
    console.print("[5] categories")
    option = Prompt.ask("[bold yellow]Opción[/bold yellow]")

    collections = {
        "1": db.users,
        "2": db.articles,
        "3": db.comments,
        "4": db.tags,
        "5": db.categories
    }
    return collections.get(option)


def create_document():
    collection = select_collection()
    if collection is None:
        console.print("[red]Opción inválida.[/red]")
        return

    # Solicitar campos y valores para el nuevo documento
    field = Prompt.ask("Ingresa el campo (por ejemplo, 'name')")
    value = Prompt.ask("Ingresa el valor del campo")
    document = {field: value}

    try:
        collection.insert_one(document)
        console.print("[green]Documento creado exitosamente![/green]")
    except pymongo.errors.PyMongoError as e:
        console.print(f"[red]Error al crear el documento: {e}[/red]")


def read_documents():
    collection = select_collection()
    if collection is None:
        console.print("[red]Opción inválida.[/red]")
        return

    documents = collection.find()
    table = Table(title="Documentos", show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Contenido")

    for doc in documents:
        table.add_row(str(doc["_id"]), str(doc))

    console.print(table)


def update_document():
    collection = select_collection()
    if collection is None:
        console.print("[red]Opción inválida.[/red]")
        return

    try:
        field = Prompt.ask("Ingresa el campo para buscar el documento (por ejemplo, 'name')")
        value = Prompt.ask("Ingresa el valor del campo para buscar")
        update_field = Prompt.ask("Ingresa el campo que deseas actualizar")
        new_value = Prompt.ask("Ingresa el nuevo valor")

        # Convertir a ObjectId si el campo es `_id`
        if field == "_id":
            value = ObjectId(value)

        # Realizar la actualización
        result = collection.update_one(
            {field: value},
            {"$set": {update_field: new_value}}
        )

        if result.modified_count > 0:
            console.print("[green]Documento actualizado correctamente![/green]")
        else:
            console.print("[yellow]No se encontró ningún documento con ese criterio o no hubo cambios.[/yellow]")
    except pymongo.errors.PyMongoError as e:
        console.print(f"[red]Error al actualizar el documento: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error inesperado: {e}[/red]")


def delete_document():
    collection = select_collection()
    if collection is None:
        console.print("[red]Opción inválida.[/red]")
        return

    try:
        field = Prompt.ask("Ingresa el campo para buscar el documento (por ejemplo, 'name')")
        value = Prompt.ask("Ingresa el valor del campo para eliminar")

        # Convertir a ObjectId si el campo es `_id`
        if field == "_id":
            value = ObjectId(value)

        # Realizar la eliminación
        result = collection.delete_one({field: value})
        if result.deleted_count > 0:
            console.print("[green]Documento eliminado correctamente![/green]")
        else:
            console.print("[yellow]No se encontró ningún documento con ese criterio.[/yellow]")
    except pymongo.errors.PyMongoError as e:
        console.print(f"[red]Error al eliminar el documento: {e}[/red]")
    except Exception as e:
        console.print(f"[red]Error inesperado: {e}[/red]")


def main():
    while True:
        choice = main_menu()
        if choice == "1":
            create_document()
        elif choice == "2":
            read_documents()
        elif choice == "3":
            update_document()
        elif choice == "4":
            delete_document()
        elif choice == "5":
            console.print("[bold red]Saliendo del programa...[/bold red]")
            break
        else:
            console.print("[red]Opción no válida, intenta de nuevo.[/red]")


if __name__ == "__main__":
    main()
