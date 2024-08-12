# Overview

This library provides an abstraction for building various network topologies such as Spine-Leaf, Fat Tree, and BCube using different link strategies. It 
is primarily used for creating topology and flow files for the NS-3 simulator. However, it can be extended to create and manage any topology format by extending the link strategy and flow strategy components.

# Components

## Network Builder

NetworkBuilder is an abstract base class designed to construct network topologies. It provides the framework for building nodes, switches, and links within a network by using various LevelConnector strategies. The subclasses implement specific network topologies like Spine-Leaf, Fat-Tree, and BCube.

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

Attributes:

connect(): Abstract method to be implemented by subclasses for connecting nodes.

final_info(): Logs the completion of the connection process.

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
    
## Link Strategy

LinkStrategy is an abstract base class designed for creating links between nodes in a network. The class provides a flexible framework for defining different linking strategies, allowing for customization in terms of bandwidth, delay, error rates, and other network parameters.

## Flow Strategy

Waiting for implementation

## Output Strategy

OutputStrategy is an abstract base class designed for data output. It allows different implementations for outputting data to various destinations, such as files or the console. This flexible design lets users choose the appropriate output strategy based on their needs.

### OutputStrategy (Abstract Base Class)
Defines the abstract method write(data: str), which must be implemented by subclasses to specify the output logic.