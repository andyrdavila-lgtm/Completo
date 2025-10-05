from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 1. Navegar a la página de login e iniciar sesión
        page.goto("http://localhost:8000/auth/login")
        page.get_by_label("Nombre de Usuario").fill("admin_demo")
        page.get_by_label("Contraseña").fill("demo123")
        page.get_by_role("button", name="Iniciar Sesión").click()

        # 2. Esperar a que cargue el dashboard y navegar a Compras
        expect(page.get_by_text("Dashboard de Cliente Demo")).to_be_visible()
        page.get_by_role("link", name="Compras").click()

        # 3. Esperar a que la página de compras cargue
        expect(page.get_by_role("heading", name="Órdenes de Compra")).to_be_visible()

        # 4. Tomar la captura de pantalla
        screenshot_path = "jules-scratch/verification/purchases_page.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)