from django.core.management.base import BaseCommand
from apps.core.services import rust_api

class Command(BaseCommand):
    help = 'Testa a conexão com o backend Rust'

    def handle(self, *args, **options):
        self.stdout.write('Testando conexão com backend Rust...')
        
        if rust_api.health_check():
            self.stdout.write(
                self.style.SUCCESS('✅ Conexão com backend Rust OK!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Falha na conexão com backend Rust')
            )
            self.stdout.write('Verifique se:')
            self.stdout.write('1. O backend Rust está rodando')
            self.stdout.write('2. A URL está correta no .env')
            self.stdout.write('3. As credenciais estão corretas')