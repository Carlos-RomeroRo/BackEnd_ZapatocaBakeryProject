EXCEL_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate",
    "Pragma": "no-cache",
}


def excel_file_headers(filename: str) -> dict[str, str]:
    return {
        **NO_CACHE_HEADERS,
        "Content-Disposition": f'attachment; filename="{filename}"',
    }
