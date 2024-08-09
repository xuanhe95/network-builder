This library provides an abstraction for building various network topologies such as Spine-Leaf, Fat Tree, and BCube using different link strategies. It is primarily used for creating topology and flow files for the NS-3 simulator. However, it can be extended to create and manage any topology format by extending the link strategy and flow strategy components.



# Components

## Topo Builder


## Level Connector

The LevelConnector class serves as an abstraction for connecting nodes across different levels of a network topology. 
The primary purpose of this class is to define the connection logic between nodes at different levels,
allowing for various connection strategies to be implemented based on specific network topology requirements.

### 1. LevelConnector (Abstract Base Class)
The LevelConnector class provides the foundation for connecting nodes between levels in a network topology. It defines an abstract method connect() that must be implemented by any subclass to specify the connection logic between nodes.

#### Attributes:

link_strategy: Strategy pattern for linking nodes.
higher_level_nodes: Nodes in the higher level to be connected.
lower_level_nodes: Nodes in the lower level to be connected.
start_id: Starting index for connecting nodes.
kwargs: Additional arguments for customization.
Methods:

connect(): Abstract method to be implemented by subclasses for connecting nodes.
finished(): Logs the completion of the connection process.
connectTo(cls, next_level_nodes, group=1): Facilitates method chaining for connecting nodes across multiple levels.
START(link_strategy, nodes, **kwargs): Static method to initiate the connection process.
END(): Finalizes the connection process.


### 2. BaseConnector (Helper Class)
The BaseConnector class is a simple implementation of the LevelConnector for method chaining. It connects nodes within a single level, making it useful for chaining connections across multiple levels.

### 3. Connection Strategies
Various subclasses of LevelConnector implement different strategies for connecting nodes:

#### OneOverStepConnector:

Connects all nodes in the upper level to groups of nodes in the lower level, with the lower level nodes connected in steps divided by the group size.
#### OneOverGroupConnector:

Connects nodes one by one in the upper level to groups in the lower level, allowing for a more distributed connection pattern.
#### GroupOverGroupConnector:

Connects groups of nodes in the upper level to corresponding groups in the lower level, facilitating a balanced and grouped connection.
#### FullMeshConnector:

Implements a full mesh connection, where every node in the upper level is connected to every node in the lower level.
#### GroupOverOneConnector:

Connects groups of nodes in the upper level to individual nodes in the lower level, ideal for scenarios where specific groupings need to connect to single nodes.

    
### Link Strategy



### Flow Strategy

### Output Strategy