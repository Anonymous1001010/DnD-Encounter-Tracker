The commands and syntax are as follows:

Roll initiative for all characters and creatures: roll
 - Rolls initiative values (1-20 inclusive) for all characters. This is a baseline, so bonuses such as Alert will have to be factored in after the fact.

roll initiative for only new characters: roll, new
 - Rolls initiative for all characters that have been added since the last initiative roll

Add a character: add, (Character Name), (HP), (AC)
 - Example: "add, John Smith
Remove a character: remove, (Character Name)
 - After removing a character, run "roll, new" to remove them from the initiative list

Modify a character: modify, (Character Name), (Desired HP), (Desired AC)

Add a condition to a character: condition, (Condition Name), (Description Of Effect), (Duration Measured In Turns), (Target Character Name)

Advance the duration of conditions by a turn: Advance
 - Example: A character afflicted with Sleep for 5 turns will have it become 4 turns when this command is used. An effect brought to 0 is automatically removed from the afflicted character.

I AM NOT AFFILIATED WITH WIZARDS OF THE COAST, THIS IS FREE TO USE BY ANYONE.
This was intended to be an all in one encounter tracker intended for DnD.
