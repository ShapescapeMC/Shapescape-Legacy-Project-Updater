(settings)=
# Configuration Settings

## Defaults
Here are the default settings of the filter.

```json
{
  "filter": "shapescape_legacy_project_updater",
  "settings": {
    "update_execute_commands": true,
    "update_block_commands": false,
    "update_summon_commands": false
  }
}
```

- `update_execute_commands` (bool): Update execute commands to the new format (from Minecraft Bedrock Edition 1.19.10 and later). Default, `true`.
- `update_block_commands` (bool): Update block commands to the new format (using block data instead of block states). Default, `true`.
- `update_summon_commands` (bool): Update summon commands to the new format (adds entity rotation to the summon command). Default, `true`.