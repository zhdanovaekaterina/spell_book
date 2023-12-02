import logging

from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, SmallInteger, Text
from sqlalchemy.orm import registry, relationship

logger = logging.getLogger(__name__)
mapper_registry = registry()
Base = mapper_registry.generate_base()


class ModelTool:
    """
    Дополнительные методы для работы с моделями
    """

    def public_attrs(self):
        return {x: y for x, y in self.__dict__.items() if not x.startswith('_')}

    def __repr__(self):
        public = self.public_attrs()

        string_pairs = [f'{key}={getattr(self, key)}' for key in public]
        attributes = ', '.join(string_pairs)
        class_name = self.__class__.__name__

        return f'<{class_name}: {attributes}>'


class School(Base, ModelTool):
    """
    Справочник по школам магии
    """

    __tablename__ = 'school'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)

    spell = relationship('Spell', back_populates='school')


class TimeToCast(Base, ModelTool):
    """
    Справочник по времени накладывания заклинания
    """

    __tablename__ = 'time_to_cast'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)

    spell = relationship('Spell', back_populates='time_to_cast')


class Distance(Base, ModelTool):
    """
    Справочник по дистанции накладывания заклинания
    """

    __tablename__ = 'distance'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False)

    spell = relationship('Spell', back_populates='distance')


class Duration(Base, ModelTool):
    """
    Справочник по длительности действия заклинания
    """

    __tablename__ = 'duration'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False)

    spell = relationship('Spell', back_populates='duration')


class Components(Base, ModelTool):
    """
    Справочник по необходимым компонентам
    """

    __tablename__ = 'components'
    alias = Column(String(32), primary_key=True)
    verbal = Column(Boolean, nullable=False, default=False)
    somatic = Column(Boolean, nullable=False, default=False)
    material = Column(Boolean, nullable=False, default=False)

    spell = relationship('Spell', back_populates='components')


class SpellType(Base, ModelTool):
    """
    Справочник по типам: атака, лечение, поддержка и т.д.
    """

    __tablename__ = 'spell_type'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)

    spell = relationship('Spell', back_populates='spell_type')


class SpellMass(Base, ModelTool):
    """
    Справочник по кол-ву попадающих под эффект: на одного, массовое, площадное
    """

    __tablename__ = 'spell_mass'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)

    spell = relationship('Spell', back_populates='spell_mass')


class SpellRoll(Base, ModelTool):
    """
    Справочник по типу броска: бросок атаки, спасбросок по определенной характеристике,
    не требует броска
    """

    __tablename__ = 'spell_roll'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)
    characteristic = Column(String(255))
    half_damage_on_success = Column(Boolean, nullable=False, default=False)

    spell = relationship('Spell', back_populates='spell_roll')


class Source(Base, ModelTool):
    """
    Справочник по источникам заклинаний
    """

    __tablename__ = 'source'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)

    spell = relationship('Spell', back_populates='source')


class Entity(Base, ModelTool):
    """
    Справочник сущностей: заклинание/заговор
    """

    __tablename__ = 'entity'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)

    spell = relationship('Spell', back_populates='entity')


class Spell(Base, ModelTool):
    """
    Справочник заклинаний - основная таблица
    """

    __tablename__ = 'spell'
    id = Column(Integer, primary_key=True, autoincrement=True)
    alias = Column(String(32), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    level = Column(Integer, nullable=False)
    school_alias = Column(String(32), ForeignKey('school.alias'), nullable=False)
    time_to_cast_alias = Column(String(32), ForeignKey('time_to_cast.alias'), nullable=False)
    distance_alias = Column(String(32), ForeignKey('distance.alias'), nullable=False)
    duration_alias = Column(String(32), ForeignKey('duration.alias'), nullable=False)
    components_alias = Column(String(32), ForeignKey('components.alias'), nullable=False)
    spell_type_alias = Column(String(32), ForeignKey('spell_type.alias'), nullable=False)
    spell_mass_alias = Column(String(32), ForeignKey('spell_mass.alias'), nullable=False)
    spell_roll_alias = Column(String(32), ForeignKey('spell_roll.alias'), nullable=False)
    source_alias = Column(String(32), ForeignKey('source.alias'), nullable=False)
    entity_alias = Column(String(32), ForeignKey('entity.alias'), nullable=False)
    concentration = Column(Boolean, nullable=False, default=False)
    ritual = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)

    school = relationship('School', back_populates='spell')
    time_to_cast = relationship('TimeToCast', back_populates='spell')
    distance = relationship('Distance', back_populates='spell')
    duration = relationship('Duration', back_populates='spell')
    components = relationship('Components', back_populates='spell')
    spell_type = relationship('SpellType', back_populates='spell')
    spell_mass = relationship('SpellMass', back_populates='spell')
    spell_roll = relationship('SpellRoll', back_populates='spell')
    source = relationship('Source', back_populates='spell')
    entity = relationship('Entity', back_populates='spell')

    effect = relationship('Effect', back_populates='spell')


class DamageType(Base, ModelTool):
    """
    Справочник по типам урона
    """

    __tablename__ = 'damage_type'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)

    effect = relationship('Effect', back_populates='damage_type')


class Effect(Base, ModelTool):
    """
    Справочник по эффектам заклинаний
    """

    __tablename__ = 'effect'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spell_id = Column(Integer, ForeignKey('spell.id'), nullable=False)
    dice_count = Column(SmallInteger, nullable=False, default=1)
    add_dice_count = Column(SmallInteger)
    dice = Column(SmallInteger, nullable=False)
    add_effect = Column(Text)
    damage_type_alias = Column(String(32), ForeignKey('damage_type.alias'), nullable=False)

    spell = relationship('Spell', back_populates='effect')
    damage_type = relationship('DamageType', back_populates='effect')


class CastType(Base, ModelTool):
    """
    Справочник по типам кастеров
    """

    __tablename__ = 'cast_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    max_cell_level = Column(SmallInteger, nullable=False)


class CellProgress(Base, ModelTool):
    """
    Справочник по росту количества ячеек
    """

    __tablename__ = 'cell_progress'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cast_type = Column(Integer, ForeignKey('cast_type.id'), nullable=False)
    class_level = Column(SmallInteger, nullable=False)
    cell_level = Column(SmallInteger, nullable=False)
    amount = Column(SmallInteger, nullable=False)


class Class(Base, ModelTool):
    """
    Справочник по классам
    """

    __tablename__ = 'class'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)
    cast_type = Column(Integer, ForeignKey('cast_type.id'), nullable=False)
    subclass_choose_level = Column(SmallInteger)
    learn_spells = Column(Boolean, nullable=False, default=False)
    prepare_spells = Column(Boolean, nullable=False, default=False)


class Subclass(Base, ModelTool):
    """
    Справочник по подклассам
    """

    __tablename__ = 'subclass'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)
    cast_type = Column(Integer, ForeignKey('cast_type.id'), nullable=False)
    class_alias = Column(String(32), ForeignKey('class.alias'), nullable=False)


class SpellAmountProgress(Base, ModelTool):
    """
    Справочник по росту количества закдлинаний для классов
    """

    __tablename__ = 'spell_amount_progress'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_alias = Column(String(32), ForeignKey('class.alias'), nullable=False)
    class_level = Column(SmallInteger, nullable=False)
    amount = Column(SmallInteger, nullable=False)
    entity = Column(String(32), ForeignKey('entity.alias'), nullable=False)


class SpellToClass(Base, ModelTool):
    """
    Many-to-many для заклинаний классов
    """

    __tablename__ = 'spell_to_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_alias = Column(String(32), ForeignKey('class.alias'), nullable=False)
    spell_id = Column(Integer, ForeignKey('spell.id'), nullable=False)


class SpellToSubclass(Base, ModelTool):
    """
    Many-to-many для заклинаний подклассов
    """

    __tablename__ = 'spell_to_subclass'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subclass_alias = Column(String(32), ForeignKey('subclass.alias'), nullable=False)
    spell_id = Column(Integer, ForeignKey('spell.id'), nullable=False)
    always_prepared = Column(Boolean, nullable=False, default=False)
