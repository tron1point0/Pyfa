# shipBonusORECapShipDroneArmorHPAndShieldHPAndHpBonus
#
# Used by:
# Ships from group: Capital Industrial Ship (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Capital Industrial Ships").level
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     type, ship.getModifiedItemAttr("shipBonusORECapital4") * level)
