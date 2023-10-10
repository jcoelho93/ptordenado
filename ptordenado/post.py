import re


class ParsedPost:
    def __init__(self, url: str, category: str, age: int, academic_level: str, years_of_experience: int, civil_status: str, dependents: int, sector: str, location: str, number_of_employees: int, multinational: bool, current_position: str, years_in_the_company: int, hours_of_work: int, shift_work: str, oncall: bool, personal_time_off: str, salary: str, monthly_gross: float, anual_gross: float) -> None:
        self.url = url
        self.category = category
        self.age = age
        self.academic_level = academic_level
        self.years_of_experience = years_of_experience
        self.civil_status = civil_status
        self.dependents = dependents
        self.sector = sector
        self.location = location
        self.number_of_employees = number_of_employees
        self.multinational = multinational
        self.current_position = current_position
        self.years_in_the_company = years_in_the_company
        self.hours_of_work = hours_of_work
        self.shift_work = shift_work
        self.oncall = oncall
        self.personal_time_off = personal_time_off
        self.salary = salary
        self.monthly_gross = monthly_gross
        self.anual_gross = anual_gross

    def parse_confidence(self):
        """Returns the number of class attributes with value None

        Returns:
            int: The number of class attributes that are None
        """
        number_of_attributes = len([attr for attr in vars(self)])
        none_attributes = len([attr for attr in vars(self) if getattr(self, attr) is None])

        return 1 - (none_attributes / number_of_attributes)

    def to_dict(self):
        return {
            "url": self.url,
            "category": self.category,
            "age": self.age,
            "academic_level": self.academic_level,
            "years_of_experience": self.years_of_experience,
            "civil_status": self.civil_status,
            "dependents": self.dependents,
            "sector": self.sector,
            "location": self.location,
            "number_of_employees": self.number_of_employees,
            "multinational": self.multinational,
            "current_position": self.current_position,
            "years_in_the_company": self.years_in_the_company,
            "hours_of_work": self.hours_of_work,
            "shift_work": self.shift_work,
            "oncall": self.oncall,
            "personal_time_off": self.personal_time_off,
            "salary": self.salary,
            "monthly_gross": self.monthly_gross,
            "anual_gross": self.anual_gross
        }


class PostParser:
    AGE_REGEX = r'(Idade ?:) ?(\d{2}).*' # Group 2 is the age
    ACADEMIC_LEVEL_REGEX = r'(Formação académica:) ?(.*)' # Group 2 is the academic level
    YEARS_OF_EXPERIENCE_REGEX = r'(Experiência profissional ?:) ?(\d{1,2})' # Group 2 is the number of years of experience
    CIVIL_STATUS_REGEX = r'(Estado civil:) ?(.*)' # Group 2 is the civil status
    DEPENDENTS_REGEX = r'(Pessoas dependentes\/filhos:) ?(\d{1,2})' # Group 2 is the number of dependents
    SECTOR_REGEX = r'(Sector\/Indústria:) (.*)' # Group 2 is the sector
    LOCATION_REGEX = r'(Cidade\/Região do Empregador:) ?(.*)' # Group 2 is the location
    NUMBER_OF_EMPLOYEES_REGEX = r'(Número de trabalhadores:) (~|\+?)(\d+)' # Group 3 is the number of employees
    MULTINATIONAL_REGEX = r'(Multinacional\?) ?(Sim|Não)' # Group 2 is the multinational
    CURRENT_POSITION_REGEX = r'(Cargo atual:) ?(.*)' # Group 2 is the current position
    YEARS_IN_THE_COMPANY_REGEX = r'(Anos na empresa atual:) ?(\d{1,2})' # Group 2 is the number of years in the company
    HOURS_OF_WORK_REGEX = r'(Horas de trabalho:) ?(\d{1,2})' # Group 2 is the number of hours of work
    SHIFT_WORK_REGEX = r'(Trabalho por turnos ou das 9h às 5h \(flexível\?\):) ?(.*)' # Group 2 is the shift work
    ONCALL_REGEX = r'(Serviço de permanência 24h:) ?(Sim|Não)' # Group 2 is the oncall
    PERSONAL_TIME_OFF_REGEX = r'(Dias de férias/ano:) ?(.*)' # Group 2 is the personal time off
    SALARY_REGEX = r'(Salário bruto\/mês \(anual\):) ?(.*)' # Group 2 is the salary
    MONTHLY_GROSS_REGEX = r'^(\d+,?\d+€?\/mês) ?\(?(\d+ ?\d+€?.+)(\)+)' # Group 1 is the monthly gross
    ANUAL_GROSS_REGEX = r'^(\d+,?\d+€?\/mês) ?\(?(\d+ ?\d+€?.+)(\)+)' # Group 2 is the anual gross

    def __init__(self, text, url: str=None, category: str=None) -> None:
        self.text = text
        self.url = url
        self.category = category

    def match_regex(self, regex, group, text=None):
        match = re.search(regex, text or self.text)
        if match:
            return self._clean_string(match.group(group))

    def _clean_string(self, string):
        return string.strip().replace('\n', '').replace('\r', '').replace("**", "")

    def parse(self) -> ParsedPost:
        age = self.match_regex(self.AGE_REGEX, 2)
        academic_level = self.match_regex(self.ACADEMIC_LEVEL_REGEX, 2)
        years_of_experience = self.match_regex(self.YEARS_OF_EXPERIENCE_REGEX, 2)
        civil_status = self.match_regex(self.CIVIL_STATUS_REGEX, 2)
        dependents = self.match_regex(self.DEPENDENTS_REGEX, 2)
        sector = self.match_regex(self.SECTOR_REGEX, 2)
        location = self.match_regex(self.LOCATION_REGEX, 2)
        number_of_employees = self.match_regex(self.NUMBER_OF_EMPLOYEES_REGEX, 3)
        multinational = self.match_regex(self.MULTINATIONAL_REGEX, 2)
        current_position = self.match_regex(self.CURRENT_POSITION_REGEX, 2)
        years_in_the_company = self.match_regex(self.YEARS_IN_THE_COMPANY_REGEX, 2)
        hours_of_work = self.match_regex(self.HOURS_OF_WORK_REGEX, 2)
        shift_work = self.match_regex(self.SHIFT_WORK_REGEX, 2)
        oncall = self.match_regex(self.ONCALL_REGEX, 2)
        personal_time_off = self.match_regex(self.PERSONAL_TIME_OFF_REGEX, 2)
        salary = self.match_regex(self.SALARY_REGEX, 2)
        monthly_gross = self.match_regex(self.MONTHLY_GROSS_REGEX, 1, salary)
        anual_gross = self.match_regex(self.ANUAL_GROSS_REGEX, 2, salary)

        return ParsedPost(
            self.url,
            self.category,
            age,
            academic_level,
            years_of_experience,
            civil_status,
            dependents,
            sector,
            location,
            number_of_employees,
            multinational,
            current_position,
            years_in_the_company,
            hours_of_work,
            shift_work,
            oncall,
            personal_time_off,
            salary,
            monthly_gross,
            anual_gross
        )
