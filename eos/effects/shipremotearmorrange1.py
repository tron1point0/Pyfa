# shipRemoteArmorRange1
#
# Used by:
# Ship: Oneiros
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGC") * level)