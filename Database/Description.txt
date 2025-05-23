**Descrição para Criação do Diagrama UML do Sistema `water_station`**

**Objetivo do Diagrama:** Representar visualmente a estrutura do banco de dados `water_station`, incluindo tabelas, seus atributos chave, e os relacionamentos entre elas com suas respectivas cardinalidades.

---

**1. Entidades (Tabelas) e Seus Atributos Principais:**

* **`AuthorizationLevel` (Nível de Autorização)**
    * **Função:** Armazena os diferentes níveis de permissão ou autorização que um usuário pode ter no sistema.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do nível de autorização.
        * `Name` (VARCHAR, UNIQUE): Nome descritivo do nível (ex: 'Administrador', 'Operador', 'Visualizador'). A unicidade garante que não haja nomes duplicados.

* **`Region` (Região)**
    * **Função:** Define as diferentes regiões geográficas ou administrativas relevantes para o sistema.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único da região.
        * `Name` (VARCHAR): Nome da região.
        * `Description` (VARCHAR): Descrição adicional sobre a região.

* **`Users` (Usuários)**
    * **Função:** Armazena informações sobre os usuários do sistema.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do usuário.
        * `Name` (VARCHAR): Nome completo do usuário.
        * `Email` (VARCHAR, UNIQUE): Endereço de e-mail do usuário, usado para login e comunicação. Deve ser único.
        * `Password` (VARCHAR): Senha do usuário (deve ser armazenada de forma segura, e.g., hash).
        * `AuthLevelID` (BIGINT, FK): Chave estrangeira referenciando `AuthorizationLevel.ID`, indicando o nível de permissão do usuário.
        * `Status` (VARCHAR): Situação do usuário (ex: 'ACTIVE', 'INACTIVE').
        * `CreatedAt`, `UpdatedAt` (TIMESTAMP): Timestamps para controle de criação e atualização.

* **`Address` (Endereço)**
    * **Função:** Armazena os detalhes dos endereços. No seu modelo, cada endereço está obrigatoriamente associado a um usuário.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do endereço.
        * `Street`, `Number`, `Neighborhood`, `State`, `City`, `Cep`, `Coordinates` (VARCHARs): Campos detalhados do endereço.
        * `UserID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `Users.ID`, indicando a qual usuário este endereço pertence.
        * `CreatedAt` (TIMESTAMP): Timestamp de criação.

* **`UserRegion` (Usuário-Região - Tabela de Junção)**
    * **Função:** Implementa a relação Muitos-para-Muitos (N:M) entre `Users` e `Region`. Um usuário pode estar associado a várias regiões, e uma região pode ter vários usuários associados.
    * **Atributos Chave:**
        * `UserID` (BIGINT, PK, FK): Chave estrangeira referenciando `Users.ID`. Parte da chave primária composta.
        * `RegionID` (BIGINT, PK, FK): Chave estrangeira referenciando `Region.ID`. Parte da chave primária composta.
        * `AssignedAt` (TIMESTAMP): Timestamp de quando a associação foi feita.

* **`Plant` (Estação de Tratamento/Operação)**
    * **Função:** Representa uma estação de tratamento, unidade de bombeamento, ou qualquer local físico de operação gerenciado pelo sistema.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único da planta.
        * `Name` (VARCHAR): Nome da planta.
        * `Type` (VARCHAR): Tipo de planta (ex: 'ETA', 'ETE', 'Reservatório Central').
        * `AddressID` (BIGINT, FK, NOT NULL, UNIQUE): Chave estrangeira referenciando `Address.ID`. Garante que cada planta tenha um endereço único.
        * `RegionID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `Region.ID`, indicando a qual região a planta pertence.
        * `Status` (VARCHAR): Situação da planta.
        * `CreatedAt` (TIMESTAMP): Timestamp de criação.

* **`ComponentType` (Tipo de Componente Hídrico)**
    * **Função:** Tabela de catálogo para definir os diferentes tipos de componentes hídricos que podem ser monitorados (Reservatório, Dessalinizador, Poço). Facilita a associação polimórfica.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do tipo de componente.
        * `Name` (VARCHAR, UNIQUE): Nome do tipo de componente (ex: 'RESERVOIR', 'DISSANILIZER', 'WATER_WELL').
        * `TableName` (VARCHAR): Nome da tabela física onde os detalhes desse tipo de componente são armazenados (ex: 'Reservoir', 'Dissanilizer'). Útil para lógica de aplicação ou triggers.
        * `Description` (VARCHAR): Descrição do tipo de componente.

* **`Reservoir` (Reservatório)**
    * **Função:** Armazena informações sobre os reservatórios.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do reservatório.
        * `Capacity` (INT): Capacidade do reservatório.
        * `Type` (VARCHAR): Tipo específico de reservatório (ex: 'Elevado', 'Enterrado').
        * `PlantID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `Plant.ID`, indicando a qual planta o reservatório pertence.
        * `ComponentTypeID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `ComponentType.ID`, classificando esta entidade como um tipo específico de componente (default para o tipo 'Reservatório').
        * `Status`, `InstallationDate`, `LastMaintenanceDate`, `CreatedAt`: Atributos de estado e auditoria.

* **`Dissanilizer` (Dessalinizador)**
    * **Função:** Armazena informações sobre os sistemas de dessalinização.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do dessalinizador.
        * `MaxAlkalinity` (INT): Capacidade ou característica do dessalinizador.
        * `PlantID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `Plant.ID`.
        * `ComponentTypeID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `ComponentType.ID` (default para o tipo 'Dessalinizador').
        * `Status`, `InstallationDate`, `LastMaintenanceDate`, `CreatedAt`: Atributos de estado e auditoria.

* **`WaterWell` (Poço de Água)**
    * **Função:** Armazena informações sobre os poços de água.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do poço.
        * `MaxFlow` (INT): Vazão máxima do poço.
        * `Depth` (DECIMAL): Profundidade do poço.
        * `PlantID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `Plant.ID`.
        * `ComponentTypeID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `ComponentType.ID` (default para o tipo 'Poço de Água').
        * `Status`, `InstallationDate`, `LastMaintenanceDate`, `CreatedAt`: Atributos de estado e auditoria.

* **`Sensor`**
    * **Função:** Armazena informações sobre os sensores físicos.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único do sensor.
        * `Name` (VARCHAR): Nome ou etiqueta do sensor.
        * `Type` (VARCHAR): Tipo de medição do sensor (ex: 'Nível', 'Vazão', 'pH').
        * `Model`, `SerialNumber` (VARCHAR): Informações do fabricante.
        * `Status`, `InstallationDate`, `CalibrationDate`, `CreatedAt`, `UpdatedAt`: Atributos de estado e auditoria.

* **`SensorComponent` (Sensor-Componente - Tabela de Associação Polimórfica)**
    * **Função:** Tabela crucial que implementa a relação entre um `Sensor` e um componente hídrico específico (`Reservoir`, `Dissanilizer`, ou `WaterWell`). Um sensor pode ser associado a exatamente um componente.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único da associação.
        * `SensorID` (BIGINT, FK, NOT NULL, UNIQUE): Chave estrangeira referenciando `Sensor.ID`. A restrição `UNIQUE` aqui é fundamental, pois garante que um sensor só pode ser listado uma vez, e, portanto, associado a apenas um componente.
        * `ComponentTypeID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `ComponentType.ID`. Indica o tipo do componente ao qual o sensor está associado (ex: se é um Reservatório, Dessalinizador ou Poço).
        * `ComponentID` (BIGINT, NOT NULL): Identificador do componente específico. Este ID se refere à coluna `ID` da tabela indicada por `ComponentTypeID` (e `ComponentType.TableName`). Por exemplo, se `ComponentTypeID` aponta para 'RESERVOIR', então `ComponentID` será um `Reservoir.ID`.
        * `AssignedAt` (TIMESTAMP): Timestamp de quando o sensor foi associado ao componente.

* **`SensorRead` (Leitura do Sensor)**
    * **Função:** Armazena os dados de leitura coletados pelos sensores.
    * **Atributos Chave:**
        * `ID` (BIGINT, PK): Identificador único da leitura.
        * `SensorID` (BIGINT, FK, NOT NULL): Chave estrangeira referenciando `Sensor.ID`, indicando qual sensor gerou esta leitura.
        * `Datetime` (DATETIME): Data e hora da leitura.
        * `Value` (DECIMAL): Valor numérico da leitura.
        * `Unit` (VARCHAR): Unidade de medida da leitura.
        * `Status` (VARCHAR): Validade da leitura (ex: 'VALID', 'INVALID', 'ESTIMATED').
        * `CreatedAt` (TIMESTAMP): Timestamp de criação.

---

**2. Relacionamentos e Cardinalidades (Como as tabelas se ligam):**

* **`AuthorizationLevel` e `Users`:**
    * `AuthorizationLevel.ID` (1) ← (`AuthLevelID`) `Users.AuthLevelID` (N)
    * **Cardinalidade:** 1:N (Um nível de autorização pode ter muitos usuários; um usuário tem um nível de autorização).
    * **Rótulo no Diagrama:** `AuthorizationLevel.ID_Users.AuthLevelID(1:N)`

* **`Users` e `Address`:**
    * `Users.ID` (1) ← (`UserID`) `Address.UserID` (N)
    * **Cardinalidade:** 1:N (Um usuário pode ter 0 ou múltiplos endereços; um endereço pertence obrigatoriamente a um usuário).
    * **Rótulo no Diagrama:** `Users.ID_Address.UserID(1:N)`

* **`Users` e `Region` (via `UserRegion`):**
    * `Users.ID` (1) ← (`UserID`) `UserRegion.UserID` (N)
    * `Region.ID` (1) ← (`RegionID`) `UserRegion.RegionID` (N)
    * **Cardinalidade:** N:M entre `Users` e `Region`.
    * **Rótulos no Diagrama:**
        * `Users.ID_UserRegion.UserID(1:N)`
        * `Region.ID_UserRegion.RegionID(1:N)`

* **`Address` e `Plant`:**
    * `Address.ID` (1) ← (`AddressID`) `Plant.AddressID` (1) (Note que `Plant.AddressID` é UNIQUE)
    * **Cardinalidade:** 1:1 (Uma planta tem exatamente um endereço; um endereço (usado por uma planta) é de exatamente uma planta).
    * **Rótulo no Diagrama:** `Plant.AddressID_Address.ID(1:1)` (Ou `Address.ID_Plant.AddressID(1:1)`)

* **`Region` e `Plant`:**
    * `Region.ID` (1) ← (`RegionID`) `Plant.RegionID` (N)
    * **Cardinalidade:** 1:N (Uma região pode ter muitas plantas; uma planta pertence a uma região).
    * **Rótulo no Diagrama:** `Region.ID_Plant.RegionID(1:N)`

* **`Plant` e `Reservoir`:**
    * `Plant.ID` (1) ← (`PlantID`) `Reservoir.PlantID` (N)
    * **Cardinalidade:** 1:N (Uma planta pode ter 0 ou muitos reservatórios; um reservatório pertence a uma planta).
    * **Rótulo no Diagrama:** `Plant.ID_Reservoir.PlantID(1:N)`

* **`Plant` e `Dissanilizer`:**
    * `Plant.ID` (1) ← (`PlantID`) `Dissanilizer.PlantID` (N)
    * **Cardinalidade:** 1:N
    * **Rótulo no Diagrama:** `Plant.ID_Dissanilizer.PlantID(1:N)`

* **`Plant` e `WaterWell`:**
    * `Plant.ID` (1) ← (`PlantID`) `WaterWell.PlantID` (N)
    * **Cardinalidade:** 1:N
    * **Rótulo no Diagrama:** `Plant.ID_WaterWell.PlantID(1:N)`

* **`ComponentType` e `Reservoir` (e `Dissanilizer`, `WaterWell`):**
    * `ComponentType.ID` (1) ← (`ComponentTypeID`) `Reservoir.ComponentTypeID` (N)
    * **Cardinalidade:** 1:N (Um tipo de componente pode classificar muitos reservatórios; um reservatório tem um tipo de componente).
    * **Rótulos no Diagrama:**
        * `ComponentType.ID_Reservoir.ComponentTypeID(1:N)`
        * `ComponentType.ID_Dissanilizer.ComponentTypeID(1:N)`
        * `ComponentType.ID_WaterWell.ComponentTypeID(1:N)`

* **`Sensor` e `SensorRead`:**
    * `Sensor.ID` (1) ← (`SensorID`) `SensorRead.SensorID` (N)
    * **Cardinalidade:** 1:N (Um sensor pode ter muitas leituras; uma leitura pertence a um sensor).
    * **Rótulo no Diagrama:** `Sensor.ID_SensorRead.SensorID(1:N)`

* **`Sensor`, `SensorComponent`, e `ComponentType` (Relação Polimórfica):**
    * **`Sensor` e `SensorComponent`:**
        * `Sensor.ID` (1) ← (`SensorID`) `SensorComponent.SensorID` (0..1) (devido à `UNIQUE(SensorID)` em `SensorComponent` e `SensorComponent.SensorID` sendo NOT NULL, mas um sensor pode não ter uma entrada em `SensorComponent` se não estiver associado)
        * **Cardinalidade:** 1 para 0..1 (Um sensor está associado a no máximo uma entrada em `SensorComponent`; uma entrada `SensorComponent` está associada a exatamente um sensor).
        * **Rótulo no Diagrama:** `Sensor.ID_SensorComponent.SensorID(1:0..1)`
    * **`ComponentType` e `SensorComponent`:**
        * `ComponentType.ID` (1) ← (`ComponentTypeID`) `SensorComponent.ComponentTypeID` (N)
        * **Cardinalidade:** 1:N (Um tipo de componente pode ser usado em muitas associações sensor-componente; cada associação especifica um tipo de componente).
        * **Rótulo no Diagrama:** `ComponentType.ID_SensorComponent.ComponentTypeID(1:N)`
    * **Ligação Polimórfica Implícita:** A coluna `SensorComponent.ComponentID` liga-se logicamente ao `ID` da tabela de componente apropriada (`Reservoir`, `Dissanilizer`, ou `WaterWell`) com base no `SensorComponent.ComponentTypeID`. Esta ligação não é uma FK direta no diagrama, mas a estrutura `ComponentType` + `ComponentID` a implementa.

---