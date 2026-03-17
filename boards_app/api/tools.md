POST mit try except

Status Codes in die jeweiligen try try und excepts unten rein schreiben mit return Response(content, status=status.HTTP_404_NOT_FOUND) um die jeweilig richtigen fehlermeldungen oder hat geklappt meldungen zu bekommen. (Unter Django restframework den passenden Status Code recherchieren)

Woher weiss serializer.save() welche def aus der serializers.py nehmen soll, zb create oder update? Es kommt einfach nur daraufan was wir mit definieren, wenn wie den serializer definieren. also bei PUT wird eine Instanz mitgegeben serializer = BoardSerializer(instanz, data) und bei PUT nur (data).

in serializers.py ein einzelnes feld validieren zb:
def validate_email(self,value):
if 'X' in value:
raise serializers.ValidationError('no X in Email')
return value

oder eine generelle def validate_letters(value) und dann in der Class beim definieren email = serializers.CharField(validators=[validate_letters]) mit einfügen.

def validate_letters(value):
errors = []
if 'X' in value:
errors.append('Please dont use the letter X')
if 'Y' in value:
errors.append('Please dont use the letter Y')
if errors:
raise serializers.ValidationError(errors)
return value

Eine Relation setzen im Modelserializer mit:
market_ids = serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), many=True, write_only=True, source='markets'))

StringRelatedField

EVtl wenn man von board auf task klickt könnt eman vllt HyperlinkedSerializer nutzen?

recht und gewerbe
rechtsschutzversicherung arag (mit nachhaltigkeitsrabatt 5% wenn ökostrom und solarzellen)
Grundbaustein + Arbeitgeber
basis komfort
premium (kollektives arbeitsrecht) mit S (55,96 mntl mit 250 euro selbstbeteiligung)
Herr Wuttke(0152 03055876)
Deniz Chen, ramirez
