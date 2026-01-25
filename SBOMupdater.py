import os
import pandas as pd
import asyncio
import json
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass
import logging
import requests

# Configuración de Logging profesional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

@dataclass
class SBOMConfig:
    """Configuración del script y rutas de archivos."""
    input_filename: str = "CONFIANZA23_SBOM_v20250830.xlsx"
    # El apiKey se gestiona internamente en el entorno de ejecución
    api_key: str = "" 
    model_id: str = "gemini-2.5-flash-preview-09-2025"
    
    @property
    def output_filename(self) -> str:
        today = datetime.now().strftime("%Y%m%d")
        return f"CONFIANZA23_SBOM_v{today}.xlsx"

class SBOMUpdater:
    """
    Clase avanzada para la actualización de SBOM con trazabilidad de celdas
    y consultas reales a modelos de lenguaje (LLM).
    """

    def __init__(self, config: SBOMConfig):
        self.config = config
        self.df: Optional[pd.DataFrame] = None

    def load_file(self) -> bool:
        """Carga el archivo Excel en un DataFrame de Pandas."""
        try:
            logger.info(f"🚀 Iniciando proceso. Abriendo archivo: {self.config.input_filename}...")
            if not os.path.exists(self.config.input_filename):
                logger.error(f"❌ Error: El archivo '{self.config.input_filename}' no fue encontrado.")
                return False
            
            self.df = pd.read_excel(self.config.input_filename)
            logger.info(f"✅ Archivo cargado. {len(self.df)} componentes detectados.")
            return True
        except Exception as e:
            logger.error(f"❌ Error crítico al cargar el archivo: {e}")
            return False

    async def fetch_latest_info_with_llm(self, component_name: str, current_version: str, row_idx: int) -> Dict[str, str]:
        """
        Consulta a Gemini para obtener información actualizada.
        Implementa reintentos con backoff exponencial.
        """
        # Prompt optimizado para respuesta JSON pura
        system_prompt = "Eres un experto en ciberseguridad y gestión de dependencias (SBOM)."
        user_query = (
            f"Componente: {component_name}. Versión actual: {current_version}. "
            "Busca la última versión estable a finales de 2025 y vulnerabilidades críticas. "
            "Responde exclusivamente en formato JSON con estas claves: "
            "'latest_version', 'status' (Secure/Vulnerable), 'notes'."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.config.model_id}:generateContent?key={self.config.api_key}"
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        # Intentos de conexión con el LLM
        for attempt in range(5):
            try:
                response = requests.post(url, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    # Extracción del texto del candidato
                    text_content = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '{}')
                    data = json.loads(text_content)
                    
                    # Notificación detallada de la actualización de la celda
                    new_ver = data.get('latest_version', current_version)
                    print(f"   📍 [Fila {row_idx + 1}] -> Actualizando Columna 'Versión_IA' con valor: {new_ver}")
                    
                    return {
                        "latest_version": new_ver,
                        "status": data.get("status", "Safe"),
                        "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                if attempt == 4: logger.debug(f"Error en fila {row_idx + 1}: {e}")
                await asyncio.sleep(2 ** attempt)

        print(f"   ⚠️ [Fila {row_idx + 1}] -> Error en consulta. Manteniendo versión original.")
        return {
            "latest_version": current_version,
            "status": "Check Manual",
            "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    async def process_updates(self):
        """Itera sobre los componentes y actualiza el DataFrame con reporte detallado."""
        if self.df is None:
            return

        logger.info("🛠️ Mapeando columnas y enviando solicitudes al LLM...")
        
        # Identificar columnas origen
        cols_map = {col.lower(): col for col in self.df.columns}
        comp_col = cols_map.get('component', 'Component')
        ver_col = cols_map.get('version', 'Version')

        tasks = []
        for index, row in self.df.iterrows():
            comp = str(row.get(comp_col, 'Unknown'))
            ver = str(row.get(ver_col, '0.0.0'))
            print(f"🔎 Procesando Fila {index + 1}: Componente '{comp}'...")
            tasks.append(self.fetch_latest_info_with_llm(comp, ver, index))

        # Ejecución de tareas
        updates = await asyncio.gather(*tasks)

        logger.info("✍️ Volcando datos de la IA en las celdas del archivo...")
        
        for i, update in enumerate(updates):
            # Reporte de actualización por celda/columna
            self.df.at[i, 'Versión_Actualizada_IA'] = update['latest_version']
            self.df.at[i, 'Estado_Seguridad'] = update['status']
            self.df.at[i, 'Fecha_Verificacion'] = update['last_checked']

    def save_file(self):
        """Graba el archivo final con formato Excel."""
        try:
            output_path = self.config.output_filename
            logger.info(f"💾 Guardando archivo actualizado en: {output_path}...")
            
            # Guardar con motor openpyxl para asegurar compatibilidad total
            self.df.to_excel(output_path, index=False, engine='openpyxl')
            
            print(f"\n" + "—"*50)
            print(f"✅ EXITO: Fichero '{output_path}' generado.")
            print(f"📊 Total de celdas actualizadas: {len(self.df) * 3}")
            print("—"*50)
        except Exception as e:
            logger.error(f"❌ Error al guardar el archivo: {e}")

async def main():
    config = SBOMConfig()
    updater = SBOMUpdater(config)
    
    if updater.load_file():
        await updater.process_updates()
        updater.save_file()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n🛑 Operación cancelada.")
    except Exception as e:
        logger.error(f"💥 Error general del sistema: {e}")