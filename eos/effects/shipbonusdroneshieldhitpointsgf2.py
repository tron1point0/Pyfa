# shipBonusDroneShieldHitpointsGF2
#
# Used by:
# Ship: Ishkur
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "shieldCapacity", ship.getModifiedItemAttr("shipBonusGF2") * level)
