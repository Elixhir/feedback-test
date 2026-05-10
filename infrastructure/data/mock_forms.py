import uuid
from datetime import datetime
from domain.constants import Language, QuestionType, FormStatus
from domain.entities.question import Question
from domain.entities.form import Form

def get_initial_forms() -> list[Form]:
    
    form1_questions = [
        Question(
            id="1",
            type=QuestionType.TEXT,
            text={
                Language.EN: "How would you describe your overall experience?",
                Language.ES: "¿Cómo describirías tu experiencia general?",
                Language.FR: "Comment décririez-vous votre expérience globale?"
            },
            required=True
        ),
        Question(
            id="2",
            type=QuestionType.MULTIPLE_CHOICE,
            text={
                Language.EN: "How did you hear about us?",
                Language.ES: "¿Cómo te enteraste de nosotros?",
                Language.FR: "Comment avez-vous entendu parler de nous?"
            },
            options=[
                {Language.EN: "Social Media", Language.ES: "Redes Sociales", Language.FR: "Réseaux Sociaux"},
                {Language.EN: "Friend/Family", Language.ES: "Amigo/Familia", Language.FR: "Ami/Famille"},
                {Language.EN: "Google Search", Language.ES: "Búsqueda Google", Language.FR: "Recherche Google"},
                {Language.EN: "Advertisement", Language.ES: "Publicidad", Language.FR: "Publicité"},
                {Language.EN: "Other", Language.ES: "Otro", Language.FR: "Autre"}
            ],
            required=False
        ),
        Question(
            id="3",
            type=QuestionType.RATING,
            text={
                Language.EN: "Rate your satisfaction (1-5)",
                Language.ES: "Califica tu satisfacción (1-5)",
                Language.FR: "Évaluez votre satisfaction (1-5)"
            },
            options=[
                {Language.EN: "1", Language.ES: "1", Language.FR: "1"},
                {Language.EN: "2", Language.ES: "2", Language.FR: "2"},
                {Language.EN: "3", Language.ES: "3", Language.FR: "3"},
                {Language.EN: "4", Language.ES: "4", Language.FR: "4"},
                {Language.EN: "5", Language.ES: "5", Language.FR: "5"}
            ],
            required=True
        ),
        Question(
            id="4",
            type=QuestionType.BOOLEAN,
            text={
                Language.EN: "Would you recommend us to a friend?",
                Language.ES: "¿Nos recomendarías a un amigo?",
                Language.FR: "Nous recommanderiez-vous à un ami?"
            },
            required=True
        ),
        Question(
            id="5",
            type=QuestionType.TEXT,
            text={
                Language.EN: "Any additional comments or suggestions?",
                Language.ES: "¿Algún comentario o sugerencia adicional?",
                Language.FR: "Commentaires ou suggestions supplémentaires?"
            },
            required=False
        )
    ]
    
    form2_questions = [
        Question(
            id="1",
            type=QuestionType.TEXT,
            text={
                Language.EN: "What is your name?",
                Language.ES: "¿Cuál es tu nombre?",
                Language.FR: "Quel est votre nom?"
            },
            required=True
        ),
        Question(
            id="2",
            type=QuestionType.TEXT,
            text={
                Language.EN: "Your email address",
                Language.ES: "Tu dirección de correo electrónico",
                Language.FR: "Votre adresse e-mail"
            },
            required=True
        ),
        Question(
            id="3",
            type=QuestionType.DATE,
            text={
                Language.EN: "When did you visit us?",
                Language.ES: "¿Cuándo nos visitaste?",
                Language.FR: "Quand nous avez-vous visité?"
            },
            required=True
        ),
        Question(
            id="4",
            type=QuestionType.SCALE,
            text={
                Language.EN: "Rate our customer service (1-10)",
                Language.ES: "Califica nuestro servicio al cliente (1-10)",
                Language.FR: "Évaluez notre service client (1-10)"
            },
            options=[
                {Language.EN: "1", Language.ES: "1", Language.FR: "1"},
                {Language.EN: "10", Language.ES: "10", Language.FR: "10"}
            ],
            required=True
        ),
        Question(
            id="5",
            type=QuestionType.MULTIPLE_CHOICE,
            text={
                Language.EN: "Which product did you purchase?",
                Language.ES: "¿Qué producto compraste?",
                Language.FR: "Quel produit avez-vous acheté?"
            },
            options=[
                {Language.EN: "Basic Plan", Language.ES: "Plan Básico", Language.FR: "Plan de Base"},
                {Language.EN: "Premium Plan", Language.ES: "Plan Premium", Language.FR: "Plan Premium"},
                {Language.EN: "Enterprise", Language.ES: "Empresarial", Language.FR: "Entreprise"}
            ],
            required=True
        ),
        Question(
            id="6",
            type=QuestionType.BOOLEAN,
            text={
                Language.EN: "Are you a returning customer?",
                Language.ES: "¿Eres cliente recurrente?",
                Language.FR: "Êtes-vous un client fidèle?"
            },
            required=True
        )
    ]
    
    form3_questions = [
        Question(
            id="1",
            type=QuestionType.RATING,
            text={
                Language.EN: "How easy was it to use our application?",
                Language.ES: "¿Qué tan fácil fue usar nuestra aplicación?",
                Language.FR: "Quelle était la facilité d'utilisation de notre application?"
            },
            options=[
                {Language.EN: "1", Language.ES: "1", Language.FR: "1"},
                {Language.EN: "2", Language.ES: "2", Language.FR: "2"},
                {Language.EN: "3", Language.ES: "3", Language.FR: "3"},
                {Language.EN: "4", Language.ES: "4", Language.FR: "4"},
                {Language.EN: "5", Language.ES: "5", Language.FR: "5"}
            ],
            required=True
        ),
        Question(
            id="2",
            type=QuestionType.TEXT,
            text={
                Language.EN: "What features would you like to see?",
                Language.ES: "¿Qué funciones te gustaría ver?",
                Language.FR: "Quelles fonctionnalités aimeriez-vous voir?"
            },
            required=False
        ),
        Question(
            id="3",
            type=QuestionType.MULTIPLE_CHOICE,
            text={
                Language.EN: "How often do you use our app?",
                Language.ES: "¿Con qué frecuencia usas nuestra app?",
                Language.FR: "Utilisez-vous notre application?"
            },
            options=[
                {Language.EN: "Daily", Language.ES: "Diariamente", Language.FR: "Quotidiennement"},
                {Language.EN: "Weekly", Language.ES: "Semanalmente", Language.FR: "Hebdomadairement"},
                {Language.EN: "Monthly", Language.ES: "Mensualmente", Language.FR: "Mensuellement"},
                {Language.EN: "Rarely", Language.ES: "Rara vez", Language.FR: "Rarement"}
            ],
            required=True
        )
    ]
    
    form4_questions = [
        Question(
            id="1",
            type=QuestionType.SCALE,
            text={Language.EN: "How likely are you to recommend us (0-10)?"},
            options=[
                {Language.EN: "0", Language.ES: "0", Language.FR: "0"},
                {Language.EN: "10", Language.ES: "10", Language.FR: "10"}
            ],
            required=True
        ),
        Question(
            id="2",
            type=QuestionType.TEXT,
            text={Language.EN: "What is the main reason for your score?"},
            required=False
        )
    ]
    
    return [
        Form(
            id=str(uuid.uuid4()),
            title={
                Language.EN: "Customer Feedback Survey",
                Language.ES: "Encuesta de Satisfacción del Cliente",
                Language.FR: "Enquête de Satisfaction Client"
            },
            description={
                Language.EN: "Help us improve by sharing your experience",
                Language.ES: "Ayúdanos a mejorar compartiendo tu experiencia",
                Language.FR: "Aidez-nous à améliorer en partageant votre expérience"
            },
            questions=form1_questions,
            version=3,
            status=FormStatus.ACTIVE.value,
            created_at=datetime(2024, 1, 15, 10, 30),
            updated_at=datetime(2024, 6, 20, 14, 45),
            created_by="admin",
            updated_by="product_manager"
        ),
        Form(
            id=str(uuid.uuid4()),
            title={
                Language.EN: "Customer Service Feedback",
                Language.ES: "Feedback de Servicio al Cliente",
                Language.FR: "Feedback Service Client"
            },
            description={
                Language.EN: "We value your opinion about our customer support",
                Language.ES: "Valamos tu opinión sobre nuestro soporte",
                Language.FR: "Votre opinion sur notre support nous est précieuse"
            },
            questions=form2_questions,
            version=1,
            status=FormStatus.ACTIVE.value,
            created_at=datetime(2024, 3, 10, 9, 0),
            updated_at=datetime(2024, 3, 10, 9, 0),
            created_by="support_team"
        ),
        Form(
            id=str(uuid.uuid4()),
            title={
                Language.EN: "Product Experience Survey",
                Language.ES: "Encuesta de Experiencia del Producto",
                Language.FR: "Enquête Expérience Produit"
            },
            description={
                Language.EN: "Share your thoughts on our product",
                Language.ES: "Comparte tus pensamientos sobre nuestro producto",
                Language.FR: "Partagez vos pensées sur notre produit"
            },
            questions=form3_questions,
            version=1,
            status=FormStatus.DRAFT.value,
            created_at=datetime(2024, 8, 1, 11, 20),
            updated_at=datetime(2024, 8, 1, 11, 20),
            created_by="product_team"
        ),
        Form(
            id=str(uuid.uuid4()),
            title={
                Language.EN: "NPS Survey",
                Language.ES: "Encuesta NPS",
                Language.FR: "Enquête NPS"
            },
            description={
                Language.EN: "Net Promoter Score survey",
                Language.ES: "Encuesta de Net Promoter Score",
                Language.FR: "Enquête Net Promoter Score"
            },
            questions=form4_questions,
            version=2,
            status=FormStatus.ARCHIVED.value,
            created_at=datetime(2023, 12, 1, 8, 0),
            updated_at=datetime(2024, 2, 15, 16, 30),
            created_by="marketing"
        )
    ]