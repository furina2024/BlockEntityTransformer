## MCDA——Minecraft Dynamic Architect

**————Structure Editor for Vanilla Animated Architecture**

Author：[奈茶泡芙](https://github.com/furina2024)

Introduction: What is Dynamic Architecture?

In Minecraft Bedrock Edition, when a block moves, it transforms into a movingblock (commonly referred to as mb) and remains in this state for 2 game ticks. During these 2 ticks, all information about the block is stored in the block entity of the mb, which acts as a container for storing special block information in the game.

Players with enough gameplay experience may notice that blocks continue to render normally while moving. This indicates that even when a block is no longer present in the world, it can still be displayed through the mb block entity. This means a block’s appearance is rendered via its mb block entity.

The position where the block recorded in the mb block entity is displayed in the game is determined by the piston (the position of the piston is recorded in the mb block entity). The block moves one block in the direction of the piston’s push or pull, depending on its state. This principle forms the foundation for dynamic architecture.

Another key feature is the nesting capability of mb. The block entity of an mb can record another mb block entity, which can further record another block. During rendering, this process forms a recursive-like structure that layers and renders blocks sequentially.

This entire process can be achieved in pure survival mode (though it’s highly complex). However, this editor is primarily aimed at creative players, so survival-specific details are omitted.

Feature 1: Structure Conversion
In this editor, click "Import Structure" to select the structure file you want to convert (it must be an .mcstructure file). After clicking "Import Structure," the file will be converted into a nested mb block entity format. You can then click "Export Structure" to select a folder and export a basic "mb projection." This projection consists of a piece of glass containing the mb block entity and a set of pistons that control its direction. Activating all pistons and moving the glass will reveal the expanded projection.

If you want the projection to remain visible, you can save it by selecting "Save as MB," but this will restrict the projection’s initial position (the glass can be moved anywhere to become an mb, but starting as an mb locks its position). You can also use certain vanilla methods to preserve the mb.

Note: In the top-left corner, the "Set Parsing Mode" option defines how the structure will be parsed.

"Minimal Path Parsing" searches for the shortest path that connects all blocks and generates a nested mb structure, maximizing space efficiency (one mb can nest up to 600 blocks; exceeding this may crash the game due to rendering overload). However, the lines may appear irregular.
"Full Position Traversal Parsing" traverses the entire rectangular range of the structure.
Feature 2: Edit Structure
Select a structure you want to edit from the table and click "Edit Structure" to open the editing window. Enter the depth you want to edit (for nested mb, depth corresponds to the specific block layer) at the top. In the block search bar, search for a block's English name to retrieve its NBT template. You can edit the values by clicking on the tree diagram. Once finished, click "Save."

Feature 3: Merge Structures
This feature allows you to merge multiple nested mb structures into one, controlled by multiple sets of pistons for different structures, even after merging. Use the dropdown menu to select the structures you want to merge, click "+," and then save to complete the merge.

Feature 4: Nest Structures
This works similarly to merging structures, but after merging, the resulting structure is controlled by a single set of pistons rather than multiple sets.

Feature 5: Move Structures
In the "Move Structure" window, select the structure you want to move. In the right-hand input field, enter the 3D coordinates of the points the building’s movement path passes through. The program will generate a curve connecting these points. Click "Save" to finalize the movement path.

Exporting Structures: Important Notes
If the structure contains more than 600 nested layers (i.e., 600 blocks), any excess blocks will automatically be deleted to prevent the game from crashing.
