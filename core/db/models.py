import logging

from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, SmallInteger, Text
from sqlalchemy.orm import registry

logger = logging.getLogger(__name__)
mapper_registry = registry()
Base = mapper_registry.generate_base()


class School(Base):
    """
    Справочник по школам магии
    """

    __tablename__ = 'school'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class TimeToCast(Base):
    """
    Справочник по времени накладывания заклинания
    """

    __tablename__ = 'time_to_cast'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class Distance(Base):
    """
    Справочник по дистанции накладывания заклинания
    """

    __tablename__ = 'distance'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class Duration(Base):
    """
    Справочник по длительности действия заклинания
    """

    __tablename__ = 'duration'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class Components(Base):
    """
    Справочник по необходимым компонентам
    """

    __tablename__ = 'components'
    id = Column(Integer, primary_key=True, autoincrement=True)
    verbal = Column(Boolean, nullable=False, default=False)
    somatic = Column(Boolean, nullable=False, default=False)
    material = Column(Boolean, nullable=False, default=False)


class SpellType(Base):
    """
    Справочник по типам: атака, лечение, поддержка и т.д.
    """

    __tablename__ = 'spell_type'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class SpellMass(Base):
    """
    Справочник по кол-ву попадающих под эффект: на одного, массовое, площадное
    """

    __tablename__ = 'spell_mass'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class SpellRoll(Base):
    """
    Справочник по типу броска: бросок атаки, спасбросок, не требует броска
    """

    __tablename__ = 'spell_roll'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class Source(Base):
    """
    Справочник по источникам заклинаний
    """

    __tablename__ = 'source'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class Entity(Base):
    """
    Справочник сущностей: заклинание/заговор
    """

    __tablename__ = 'entity'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class Spell(Base):
    """
    Справочник заклинаний - основная таблица
    """

    __tablename__ = 'spell'
    id = Column(Integer, primary_key=True, autoincrement=True)
    alias = Column(String(32), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    level = Column(Integer, nullable=False)
    school = Column(String(32), ForeignKey('school.alias'), nullable=False)
    time_to_cast = Column(String(32), ForeignKey('time_to_cast.alias'), nullable=False)
    distance = Column(String(32), ForeignKey('distance.alias'), nullable=False)
    duration = Column(String(32), ForeignKey('duration.alias'), nullable=False)
    components = Column(Integer, ForeignKey('components.id'), nullable=False)
    spell_type = Column(String(32), ForeignKey('spell_type.alias'), nullable=False)
    spell_mass = Column(String(32), ForeignKey('spell_mass.alias'), nullable=False)
    spell_roll = Column(String(32), ForeignKey('spell_roll.alias'), nullable=False)
    source = Column(String(32), ForeignKey('source.alias'), nullable=False)
    entity = Column(String(32), ForeignKey('entity.alias'), nullable=False)
    concentration = Column(Boolean, nullable=False, default=False)
    ritual = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)


class DamageType(Base):
    """
    Справочник по типам урона
    """

    __tablename__ = 'damage_type'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)


class CountripEffect(Base):
    """
    Справочник по эффектам заговоров
    """

    __tablename__ = 'countrip_effect'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spell_id = Column(Integer, ForeignKey('spell.id'), nullable=False)
    caster_level = Column(SmallInteger, nullable=False, default=1)
    dice_count = Column(SmallInteger, nullable=False, default=1)
    dice = Column(SmallInteger, nullable=False)
    damage_type = Column(String(32), ForeignKey('damage_type.alias'), nullable=False)


class SpellEffect(Base):
    """
    Справочник по эффектам заклинаний
    """

    __tablename__ = 'spell_effect'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spell_id = Column(Integer, ForeignKey('spell.id'), nullable=False)
    cell_level = Column(SmallInteger, nullable=False, default=1)
    dice_count = Column(SmallInteger, nullable=False, default=1)
    dice = Column(SmallInteger, nullable=False)
    damage_type = Column(String(32), ForeignKey('damage_type.alias'), nullable=False)


class CastType(Base):
    """
    Справочник по типам кастеров
    """

    __tablename__ = 'cast_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    max_cell_level = Column(SmallInteger, nullable=False)
    learn_spells = Column(Boolean, nullable=False, default=False)
    prepare_spells = Column(Boolean, nullable=False, default=False)


class CellProgress(Base):
    """
    Справочник по росту количества ячеек
    """

    __tablename__ = 'cell_progress'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cast_type = Column(Integer, ForeignKey('cast_type.id'), nullable=False)
    class_level = Column(SmallInteger, nullable=False)
    cell_level = Column(SmallInteger, nullable=False)
    amount = Column(SmallInteger, nullable=False)


class Class(Base):
    """
    Справочник по классам
    """

    __tablename__ = 'class'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)
    cast_type = Column(Integer, ForeignKey('cast_type.id'), nullable=False)
    subclass_choose_level = Column(SmallInteger)


class Subclass(Base):
    """
    Справочник по подклассам
    """

    __tablename__ = 'subclass'
    alias = Column(String(32), primary_key=True)
    title = Column(String(255), nullable=False)
    cast_type = Column(Integer, ForeignKey('cast_type.id'), nullable=False)
    class_alias = Column(String(32), ForeignKey('class.alias'), nullable=False)


class SpellAmountProgress(Base):
    """
    Справочник по росту количества закдлинаний для классов
    """

    __tablename__ = 'spell_amount_progress'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_alias = Column(String(32), ForeignKey('class.alias'), nullable=False)
    class_level = Column(SmallInteger, nullable=False)
    amount = Column(SmallInteger, nullable=False)
    entity = Column(String(32), ForeignKey('entity.alias'), nullable=False)


class SpellToClass(Base):
    """
    Many-to-many для заклинаний классов
    """

    __tablename__ = 'spell_to_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_alias = Column(String(32), ForeignKey('class.alias'), nullable=False)
    spell_id = Column(Integer, ForeignKey('spell.id'), nullable=False)


class SpellToSubclass(Base):
    """
    Many-to-many для заклинаний подклассов
    """

    __tablename__ = 'spell_to_subclass'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subclass_alias = Column(String(32), ForeignKey('subclass.alias'), nullable=False)
    spell_id = Column(Integer, ForeignKey('spell.id'), nullable=False)
    always_prepared = Column(Boolean, nullable=False, default=False)
