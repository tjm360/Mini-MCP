from mcp.server import MCPServer
import os
from pathlib import Path

# MCP-Server initialisieren
mcp = MCPServer("Taschenrechner")

# Tool: Addition
@mcp.tool()
def add(a: int, b: int) -> int:
    """Addiert zwei Zahlen"""
    return a + b

# Resource: Inhalt von pysdk.md bereitstellen
@mcp.resource("file://{filename}")
async def get_file(filename: str) -> str:
    if filename == "pysdk.md":
        desktop_path = Path.home() / "Desktop"
        file_path = desktop_path / filename
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error reading {filename}: {str(e)}"
    return "Datei nicht erlaubt"

@mcp.resource("file://pysdk.md")
async def pysdkfile() -> str:
    desktop_path = Path.home() / "Desktop"
    file_path = desktop_path / "pysdk.md"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading pysdk.md: {str(e)}"

# MCP Prompt: meeting_prompt
@mcp.prompt()
def meeting_prompt(meeting_date: str, meeting_title: str, transcript: str) -> str:
    """Erstellt eine Besprechungszusammenfassung basierend auf dem Template aus meeting_prompt.md."""
    template_path = Path(__file__).parent / "meeting_prompt.md"
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except Exception as e:
        return f"Fehler beim Laden des Templates: {str(e)}"
    # Template-Variablen ersetzen
    result = template.replace("{{ meeting_date }}", meeting_date)
    result = result.replace("{{ meeting_title }}", meeting_title)
    result = result.replace("{{ transcript }}", transcript)
    return result

if __name__ == "__main__":
    transport = os.getenv("TRANSPORT", "stdio")
    if transport == "sse":
        mcp.run(
            transport="sse",
            host=os.getenv("HOST", "127.0.0.1"),
            port=int(os.getenv("PORT", "3000")),
        )
    else:
        mcp.run()