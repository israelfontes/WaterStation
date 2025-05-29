#!/usr/bin/env python3
"""
Simulador Simples de Sensor
Para testes rápidos da API
"""

import requests
import time
import random
from datetime import datetime

class SimpleSensor:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
    
    def login(self, username="admin@waterstation.com", password="admin123"):
        """Login na API"""
        url = f"{self.base_url}/api/users/token/"
        data = {"email": username, "password": password}
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                self.token = response.json()['access']
                self.headers['Authorization'] = f'Bearer {self.token}'
                print("✅ Login realizado")
                return True
            else:
                print(f"❌ Erro no login: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def health_check(self):
        """Verificar se API está online"""
        try:
            response = requests.get(f"{self.base_url}/api/monitoring/health/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API Online - {data['statistics']['sensors_active']} sensores ativos")
                return True
            else:
                print(f"❌ API Offline: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def send_reading(self, sensor_id, value):
        """Enviar leitura única"""
        url = f"{self.base_url}/api/monitoring/sensor-data/"
        data = {
            "sensor_id": sensor_id,
            "value": value
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            if response.status_code == 201:
                result = response.json()
                status = result.get('status', 'normal')
                warning = result.get('warning', '')
                
                if warning:
                    print(f"⚠️  Sensor {sensor_id}: {value} - {warning}")
                else:
                    print(f"✅ Sensor {sensor_id}: {value} enviado")
                return True
            else:
                print(f"❌ Erro: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def simulate_sensor(self, sensor_id, sensor_type="temperature", duration=60):
        """Simular um sensor por X segundos"""
        print(f"🔄 Simulando sensor {sensor_id} ({sensor_type}) por {duration}s...")
        
        # Valores base por tipo de sensor
        sensor_ranges = {
            'temperature': (20.0, 30.0),
            'ph': (6.5, 8.5), 
            'salinity': (500, 1500),
            'flow': (200, 400),
            'pressure': (3.0, 5.0),
            'level': (70, 95)
        }
        
        min_val, max_val = sensor_ranges.get(sensor_type, (0, 100))
        current_value = random.uniform(min_val, max_val)
        
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < duration:
                # Gerar valor próximo ao anterior (mais realista)
                change = random.uniform(-0.1, 0.1) * (max_val - min_val)
                current_value += change
                
                # Manter nos limites
                current_value = max(min_val, min(max_val, current_value))
                
                # Enviar leitura
                self.send_reading(sensor_id, round(current_value, 2))
                
                # Aguardar
                time.sleep(10)  # 10 segundos entre leituras
                
        except KeyboardInterrupt:
            print("\n🛑 Simulação interrompida")

def main():
    print("🔧 Simulador Simples de Sensor")
    print("=" * 35)
    
    sensor = SimpleSensor()
    
    # 2. Login
    print("\n2️⃣ Fazendo login...")
    if not sensor.login():
        print("❌ Não foi possível fazer login")
        return
    
    # 3. Menu de opções
    print("\n3️⃣ Opções de simulação:")
    print("1. Simular sensor de temperatura (ID: 1)")
    print("2. Simular sensor de pH (ID: 2)")  
    print("3. Simular sensor de salinidade (ID: 3)")
    print("4. Enviar leitura única")
    print("5. Teste de múltiplos sensores")
    
    try:
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == "1":
            sensor.simulate_sensor(1, "temperature", 120)
        elif choice == "2":
            sensor.simulate_sensor(2, "ph", 120)
        elif choice == "3":
            sensor.simulate_sensor(3, "salinity", 120)
        elif choice == "4":
            sensor_id = int(input("ID do sensor: "))
            value = float(input("Valor: "))
            sensor.send_reading(sensor_id, value)
        elif choice == "5":
            # Teste múltiplos sensores
            print("🔄 Testando múltiplos sensores...")
            sensors = [
                (1, "temperature"),
                (2, "ph"),
                (3, "salinity")
            ]
            
            for i in range(10):  # 10 ciclos
                print(f"\n📡 Ciclo {i+1}/10")
                for sensor_id, sensor_type in sensors:
                    if sensor_type == "temperature":
                        value = round(random.uniform(20, 30), 1)
                    elif sensor_type == "ph":
                        value = round(random.uniform(6.5, 8.5), 1)
                    else:  # salinity
                        value = round(random.uniform(500, 1500), 0)
                    
                    sensor.send_reading(sensor_id, value)
                    time.sleep(2)
                
                time.sleep(5)  # Aguardar entre ciclos
        else:
            print("❌ Opção inválida")
    
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()