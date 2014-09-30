# shipSHTDmgBonusRookie
#
# Used by:
# Ship: Velator
# Ship: Violator
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("rookieSHTDamageBonus"))
