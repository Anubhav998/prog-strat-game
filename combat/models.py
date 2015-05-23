from django.db import models


class Conflict(models.Model):
    territory = models.ForeignKey('arenas.Territory')
    aggressor = models.ForeignKey('profiles.Profile', related_name='invasions')
    defender = models.ForeignKey('profiles.Profile', related_name='defenses', blank=True, null=True)
    start_turn = models.IntegerField()
    complete_turn = models.IntegerField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    victory = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return "Conflict"

    def represent(self):
        aggressors = sorted(self.aggressorunit_set.all(), key=lambda u: u.unit.defence)
        defenders = sorted(self.defenderunit_set.all(), key=lambda u: u.unit.defence)
        formatted_aggressors = [unit.unit.get_power_display() for unit in aggressors]
        formatted_defenders = [unit.unit.get_power_display() for unit in defenders]
        return "[%s]v[%s]" % (",".join(formatted_aggressors), ",".join(formatted_defenders))

    def check_complete(self, turn):
        if self.aggressorunit_set.count() == 0:
            self.complete = True
            self.complete_turn = turn
            self.victory = False
            self.save()
            return True
        battle_status = self.get_total_offence() - self.get_total_defence()
        if battle_status >= self.territory.territorydetail.acquisition:
            self.complete = True
            self.complete_turn = turn
            self.victory = True
            self.save()
            return True
        return False

    def get_total_offence(self):
        return sum([unit.unit.attack for unit in self.aggressorunit_set.all()])

    def get_total_defence(self):
        return sum([unit.unit.defence for unit in self.defenderunit_set.all()])

    def resolve(self):
        aggressors = sorted(self.aggressorunit_set.all(), key=lambda u: u.unit.defence)
        defenders = sorted(self.defenderunit_set.all(), key=lambda u: u.unit.defence)
        aggressor_total_offence = sum([unit.unit.attack for unit in aggressors])
        defender_total_offence = sum([unit.unit.attack for unit in defenders])
        while len(aggressors) > 0 and defender_total_offence > 0:
            unit = aggressors[0]
            if defender_total_offence >= unit.unit.defence:
                unit.delete()
                aggressors.pop(0)
                defender_total_offence -= unit.unit.defence
            else:
                break
        while len(defenders) > 0 and aggressor_total_offence > 0:
            unit = defenders[0]
            if aggressor_total_offence >= unit.unit.defence:
                unit.delete()
                defenders.pop(0)
                aggressor_total_offence -= unit.unit.defence
            else:
                break


class AggressorUnit(models.Model):
    conflict = models.ForeignKey(Conflict)
    unit = models.ForeignKey('military.Unit')


class DefenderUnit(models.Model):
    conflict = models.ForeignKey(Conflict)
    unit = models.ForeignKey('military.Unit')
