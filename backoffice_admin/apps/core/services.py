import requests
import logging
from django.conf import settings
from django.core.cache import cache
from typing import Dict, Any, Optional
import json

logger = logging.getLogger('rust_api')

class RustAPIService:
    """Serviço para comunicação com o backend Rust"""
    
    def __init__(self):
        self.base_url = settings.API_SETTINGS['RUST_API_BASE_URL']
        self.timeout = settings.API_SETTINGS['API_TIMEOUT']
        self.retries = settings.API_SETTINGS['API_RETRIES']
        self.api_key = settings.RUST_API_KEY
        self.api_secret = settings.RUST_API_SECRET
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers padrão para requisições"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        
        return headers
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Optional[Dict]:
        """Faz requisição para a API Rust com retry"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        for attempt in range(self.retries):
            try:
                logger.info(f"Tentativa {attempt + 1}: {method} {url}")
                
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params,
                    timeout=self.timeout
                )
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro na tentativa {attempt + 1}: {e}")
                if attempt == self.retries - 1:
                    logger.error(f"Falha após {self.retries} tentativas")
                    return None
        
        return None
    
    def get(self, endpoint: str, params: Optional[Dict] = None, use_cache: bool = True) -> Optional[Dict]:
        """GET request com cache opcional"""
        cache_key = f"rust_api_{endpoint}_{hash(str(params))}" if use_cache else None
        
        if use_cache and cache_key:
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info(f"Cache hit para {endpoint}")
                return cached_data
        
        data = self._make_request('GET', endpoint, params=params)
        
        if data and use_cache and cache_key:
            cache.set(cache_key, data, timeout=300)  # 5 minutos
        
        return data
    
    def post(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """POST request"""
        return self._make_request('POST', endpoint, data=data)
    
    def put(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """PUT request"""
        return self._make_request('PUT', endpoint, data=data)
    
    def delete(self, endpoint: str) -> Optional[Dict]:
        """DELETE request"""
        return self._make_request('DELETE', endpoint)
    
    # Métodos específicos para o e-commerce
    def get_properties(self, page: int = 1, limit: int = 20) -> Optional[Dict]:
        """Busca propriedades do backend Rust"""
        params = {'page': page, 'limit': limit}
        return self.get('properties', params=params)
    
    def get_property(self, property_id: int) -> Optional[Dict]:
        """Busca uma propriedade específica"""
        return self.get(f'properties/{property_id}')
    
    def create_property(self, property_data: Dict) -> Optional[Dict]:
        """Cria uma nova propriedade"""
        return self.post('properties', property_data)
    
    def update_property(self, property_id: int, property_data: Dict) -> Optional[Dict]:
        """Atualiza uma propriedade"""
        return self.put(f'properties/{property_id}', property_data)
    
    def delete_property(self, property_id: int) -> Optional[Dict]:
        """Deleta uma propriedade"""
        return self.delete(f'properties/{property_id}')
    
    def get_users(self, page: int = 1, limit: int = 20) -> Optional[Dict]:
        """Busca usuários do backend Rust"""
        params = {'page': page, 'limit': limit}
        return self.get('users', params=params)
    
    def health_check(self) -> bool:
        """Verifica se o backend Rust está funcionando"""
        try:
            response = self.get('health', use_cache=False)
            return response is not None
        except:
            return False

# Instância global do serviço
rust_api = RustAPIService()