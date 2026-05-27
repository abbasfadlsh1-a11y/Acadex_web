import flet as ft
import os
import ssl
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
os.environ["PYTHONWARNINGS"] = "ignore"

from main_logic import AppController
from organize import check_solve_limit

def main(page: ft.Page):
    page.on_error = lambda e: print("Flet Error:", e.data)
    ssl.create_default_https_context = ssl._create_unverified_context

    page.title = "Acadex App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 420
    page.window_height = 730
    page.padding = 20

    status_label = ft.Text(value="No media attached", size=11, italic=True)
    text_input = ft.TextField(label="Type your question", hint_text="Type here...", multiline=True)
    solution_output = ft.Text(value="The AI solution will appear here...")
    controller = AppController()

    def pick_result(e):
        if e.files:
            status_label.value = f"File: {e.files[0].path}"
            page.update()

    file_picker = ft.FilePicker()
    file_picker.on_result=pick_result
    page.services.append(file_picker)

    async def handle_attach_file(e):
        await file_picker.pick_files(allow_multiple=False)

    async def handle_attach_image(e):
        await file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"]
        )

    async def handle_open_camera(e):
        await file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"]
        )

    def handle_execute(e):
        has_image = "File:" in status_label.value or "Image:" in status_label.value
        allowed, message = check_solve_limit(has_image=has_image)
        if not allowed:
            solution_output.value = message if message else "Access denied: limit reached."
            page.update()
            return
        solution_output.value = "Processing your request... Please wait."
        page.update()
        try:
            file_path = None
            if has_image:
                file_path = ststus_label.value.replace("File: ","").replace("Image: ","")
            result = controller.execute_process(text_input.value, file_path)
            solution_output.value = result
        except Exception as ex:
            solution_output.value = f"Error: {str(ex)}"
        page.update()

    def handle_save_solution(e):
        if "will appear here" in solution_output.value:
            status_label.value = "Nothing to save yet!"
        else:
            status_label.value = "Solution saved to history!"
        page.update()

    input_row = ft.Row([
        text_input,
        ft.IconButton(icon=ft.Icons.ADD, on_click=handle_attach_file),
        ft.IconButton(icon=ft.Icons.CAMERA_ALT, on_click=handle_open_camera),
        ft.IconButton(icon=ft.Icons.IMAGE, on_click=handle_attach_image),
    ])

    solution_container = ft.Container(
        content=solution_output,
        height=200,
        padding=15,
    )

    execute_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.PLAY_ARROW), ft.Text("Solve with AI")],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        on_click=handle_execute
    )

    save_btn = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.SAVE), ft.Text("Save Solution")],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        on_click=handle_save_solution
    )

    page.add(ft.Column([
        ft.Text("Acadex Suite", size=24, weight="bold"),
        status_label,
        input_row,
        solution_container,
        ft.Row(
            [execute_btn, save_btn],
            alignment=ft.MainAxisAlignment.CENTER
        )
    ], scroll=ft.ScrollMode.ADAPTIVE))

    page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
