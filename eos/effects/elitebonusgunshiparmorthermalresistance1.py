# eliteBonusGunshipArmorThermalResistance1
#
# Used by:
# Ship: Vengeance
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Assault Frigates").level
    fit.ship.boostItemAttr("armorThermalDamageResonance", ship.getModifiedItemAttr("eliteBonusGunship1") * level)