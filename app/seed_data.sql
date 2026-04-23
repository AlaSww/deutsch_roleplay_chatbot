BEGIN;

INSERT INTO public.users (id, email, password_hash, plan, german_level, native_language)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'amina@example.com', 'scrypt:32768:8:1$Db9nGllJm76l8HLL$98c2333d34cf55c743562882cfdd94d233301a7f053a01f2da6fb80e6f54b44be3344698de9072123e60c02ed6f9278791dc0df92296b1c0a23451cd35d46bcd', 'free', 'A1', 'Arabic'),
    ('22222222-2222-2222-2222-222222222222', 'samir@example.com', 'scrypt:32768:8:1$C4CYqYW6kpwe4Jzp$875f71929109936f5522a28913140d83245d591692b7ffc329fe9d4f1c910045187fd9dc509e6859ffc14bf7ba08e2558d102b2eafc6dfdcf75e75011e50ba79', 'free', 'B1', 'French'),
    ('33333333-3333-3333-3333-333333333333', 'laura@example.com', 'scrypt:32768:8:1$9cS1Uk0zxMSRSHCB$2116d27582bc40e2df9a9ba24c7ced3dbca4aa7b83ebc4ceae134c50dae93da092b510ab4c5c8b27f180e135016bd1d70670d6d5ad81ca6c24e905babd8cc35c', 'premium', 'C1', 'English')
ON CONFLICT (id) DO UPDATE
SET
    email = EXCLUDED.email,
    password_hash = EXCLUDED.password_hash,
    plan = EXCLUDED.plan,
    german_level = EXCLUDED.german_level,
    native_language = EXCLUDED.native_language;

INSERT INTO public.user_profiles (
    id,
    user_id,
    common_mistakes,
    grammar_focus_areas,
    vocabulary_gaps,
    strengths,
    last_feedback_summary
)
VALUES
    (
        '44444444-4444-4444-4444-444444444441',
        '11111111-1111-1111-1111-111111111111',
        '["verb position in main clauses", "article gender confusion", "missing capitalization for nouns"]'::jsonb,
        '["present tense sentence order", "accusative articles", "basic question forms"]'::jsonb,
        '["ordering food items", "drink sizes", "common cafe phrases"]'::jsonb,
        '["good basic greetings", "clear simple requests", "willingness to continue the conversation"]'::jsonb,
        'Amina communicates clearly at beginner level but still needs reminders about article choice and German word order.'
    ),
    (
        '44444444-4444-4444-4444-444444444442',
        '22222222-2222-2222-2222-222222222222',
        '["case endings after prepositions", "word order in subordinate clauses"]'::jsonb,
        '["dative vs accusative", "weil and dass clauses", "natural connector usage"]'::jsonb,
        '["apartment rental terms", "lease vocabulary", "neighborhood descriptions"]'::jsonb,
        '["asks relevant follow-up questions", "good conversational flow", "solid intermediate vocabulary"]'::jsonb,
        'Samir is comfortable in practical conversations and should focus on more accurate case usage and clause structure.'
    ),
    (
        '44444444-4444-4444-4444-444444444443',
        '33333333-3333-3333-3333-333333333333',
        '["occasional register mismatch in formal settings", "minor collocation errors"]'::jsonb,
        '["formal interview phrasing", "idiomatic professional language"]'::jsonb,
        '["HR vocabulary", "salary negotiation language"]'::jsonb,
        '["strong fluency", "natural sentence variety", "good self-correction"]'::jsonb,
        'Laura is advanced and should mainly polish formality, precision, and more native-like collocations in professional contexts.'
    )
ON CONFLICT (user_id) DO UPDATE
SET
    common_mistakes = EXCLUDED.common_mistakes,
    grammar_focus_areas = EXCLUDED.grammar_focus_areas,
    vocabulary_gaps = EXCLUDED.vocabulary_gaps,
    strengths = EXCLUDED.strengths,
    last_feedback_summary = EXCLUDED.last_feedback_summary,
    updated_at = NOW();

INSERT INTO public.scenarios (id, name, description, prompt_context, is_premium)
VALUES
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1',
        'Cafe Visit',
        'A conversation in a German cafe where one person is ordering and the other is helping with the order.',
        'This roleplay happens in a busy but friendly cafe in Berlin around lunchtime. One participant is a customer and the other is a cafe worker. The conversation should naturally cover greetings, ordering food or drinks, clarifying details, asking follow-up questions, and finishing the interaction politely.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2',
        'Apartment Viewing',
        'A conversation during an apartment viewing where one person is offering the apartment and the other is evaluating it.',
        'This roleplay happens during an apartment viewing in Munich. One participant is showing or representing the apartment and the other is interested in renting it. The conversation should naturally include rent, rooms, deposit, furniture, neighborhood, lease conditions, and practical living questions.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3',
        'Job Interview',
        'A formal conversation between a job interviewer and a candidate.',
        'This roleplay is a realistic first-round job interview in Germany for an office-based role. One participant is the interviewer and the other is the candidate. The conversation should include introductions, experience, strengths, motivation, teamwork, availability, and other realistic interview topics.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa4',
        'Doctor Appointment',
        'A conversation during a medical appointment between a doctor and a patient.',
        'This roleplay takes place during a routine doctor visit in Hamburg. One participant is the doctor and the other is the patient. The conversation should naturally include symptoms, duration, pain, medication, follow-up questions, and next steps in a calm and realistic tone.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa5',
        'Train Station Help',
        'A conversation at a German train station between a traveler and a service agent.',
        'This roleplay happens at a train station service desk in Germany. One participant needs travel help and the other provides assistance. The conversation should naturally cover delays, missed trains, ticket questions, platform information, luggage concerns, and polite requests for help.',
        false
    )
ON CONFLICT (id) DO UPDATE
SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    prompt_context = EXCLUDED.prompt_context,
    is_premium = EXCLUDED.is_premium;

INSERT INTO public.scenario_roles (id, scenario_id, role_name, prompt_context)
VALUES
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb101',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1',
        'Customer',
        'You are the customer in a German cafe. You want to order something, ask follow-up questions when needed, and respond naturally to what the staff says.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb102',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1',
        'Cafe Worker',
        'You work in the cafe and help the customer place the order. You greet them, answer questions, clarify details, and keep the interaction realistic and efficient.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb201',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2',
        'Prospective Tenant',
        'You are interested in renting the apartment. You ask about price, conditions, rooms, furniture, location, and anything important before deciding.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb202',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2',
        'Landlord',
        'You are showing the apartment or representing the owner. You answer questions, explain the apartment clearly, and ask the prospective tenant relevant follow-up questions.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb301',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3',
        'Candidate',
        'You are applying for the job. You introduce yourself, describe your background, answer interview questions, and ask thoughtful questions when appropriate.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb302',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3',
        'Interviewer',
        'You are conducting the interview. You ask realistic interview questions, follow up on answers, and keep the interaction professional and natural.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb401',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa4',
        'Patient',
        'You are visiting the doctor because of a health problem. You describe symptoms, answer questions, and ask for clarification or advice when needed.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb402',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa4',
        'Doctor',
        'You are the doctor. You ask careful questions, react to the patient’s answers, explain things clearly, and keep the interaction calm and realistic.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb501',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa5',
        'Traveler',
        'You need help at the train station. You ask questions about your train, ticket, platform, delay, or next connection and respond naturally to assistance.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb502',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa5',
        'Service Agent',
        'You work at the train station service desk. You help the traveler solve travel problems clearly, politely, and practically.'
    )
ON CONFLICT (id) DO UPDATE
SET
    scenario_id = EXCLUDED.scenario_id,
    role_name = EXCLUDED.role_name,
    prompt_context = EXCLUDED.prompt_context;

COMMIT;
