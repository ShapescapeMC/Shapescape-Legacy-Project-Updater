(installation)=
# Installation

## Steps

### 1. Install the filter
Use the following command
```
regolith install shapescape_legacy_project_updater
```

You can alternatively use this command:
```
regolith install github.com/ShapescapeMC/Shapescape-Legacy-Project-Updater/shapescape_legacy_project_updater
```

### 2. Add filter to a profile
Add the filter to the `filters` list in the `config.json` file of the Regolith project and add the settings:

```json
{
  "filter": "shapescape_legacy_project_updater"
}
```