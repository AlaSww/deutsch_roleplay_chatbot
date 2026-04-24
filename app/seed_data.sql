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
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa6',
        'Team Meeting Update',
        'A workplace conversation where one colleague gives a project update and the other asks follow-up questions.',
        'This roleplay happens during a short project status meeting in a German-speaking office. One participant gives a structured update on progress, blockers, deadlines, and next steps, while the other asks clarifying questions and reacts professionally.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa7',
        'Client Kickoff Call',
        'A professional call between a company representative and a new client starting a project.',
        'This roleplay is a first kickoff call for a new project with a German-speaking client. The conversation should include introductions, goals, scope, expectations, timing, deliverables, responsibilities, and polite business language.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa8',
        'Performance Review',
        'A formal review conversation between a manager and an employee.',
        'This roleplay is a structured performance review in a German-speaking company. The conversation should naturally include strengths, challenges, recent results, feedback, goals, training needs, and future expectations in a respectful tone.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa9',
        'Salary Negotiation',
        'A formal salary discussion between an employee or candidate and a manager or recruiter.',
        'This roleplay is a realistic salary discussion in a professional German context. The conversation should include responsibilities, market value, achievements, expectations, numbers, benefits, compromise, and polite negotiation language.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa10',
        'Technical Support Ticket',
        'A problem-solving conversation between an employee and an IT support specialist.',
        'This roleplay happens when an employee contacts internal IT support in German. The conversation should cover the technical problem, urgency, troubleshooting steps, system details, access issues, and next actions clearly and efficiently.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa11',
        'Job Interview Follow-up',
        'A professional follow-up conversation after an interview between a recruiter and a candidate.',
        'This roleplay takes place after a first interview round. The participants discuss impressions, next steps, availability, documents, salary expectations, and any open questions in a formal but friendly business tone.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa12',
        'Onboarding First Day',
        'A workplace orientation conversation between a new employee and a team lead or colleague.',
        'This roleplay happens on the first working day at a German-speaking company. The conversation should include introductions, company routines, tools, team structure, expectations, scheduling, and practical onboarding questions.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa13',
        'Product Demo',
        'A sales-oriented conversation where one participant presents a product and the other evaluates it.',
        'This roleplay is a product demo for a business customer. The conversation should include needs analysis, product features, pricing logic, implementation questions, objections, benefits, and next steps using clear professional German.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa14',
        'Project Deadline Problem',
        'A workplace conversation about a deadline risk between a project member and a manager or client.',
        'This roleplay happens when a project is at risk of delay. The conversation should naturally cover causes, dependencies, revised timing, mitigation plans, responsibility, communication strategy, and professionally managing expectations.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa15',
        'Conference Networking',
        'A semi-formal professional networking conversation between two attendees at an industry event.',
        'This roleplay takes place at a professional conference in Germany. The conversation should include introductions, job roles, company background, shared interests, industry topics, possible collaboration, and polite closing language.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa16',
        'Business Travel Check-in',
        'A professional travel-related conversation between a business traveler and a hotel receptionist.',
        'This roleplay happens during a hotel check-in for a business trip in Germany. The conversation should include reservation details, company booking, invoice requests, breakfast, Wi-Fi, meeting timing, and practical travel questions.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa17',
        'Vendor Negotiation',
        'A procurement-style conversation between a buyer and a supplier representative.',
        'This roleplay is a realistic procurement discussion in German. The conversation should include pricing, quantities, delivery deadlines, contract conditions, reliability, discounts, quality expectations, and professional negotiation language.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa18',
        'Marketing Campaign Planning',
        'A planning conversation between a marketing manager and a specialist or agency contact.',
        'This roleplay happens during planning for a new campaign. The conversation should cover target audience, channels, budget, content deadlines, KPIs, risks, responsibilities, and approval processes in practical business German.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa19',
        'Customer Complaint Resolution',
        'A professional service conversation between an unhappy customer and a company representative.',
        'This roleplay involves handling a serious customer complaint in German. The conversation should include listening carefully, clarifying the issue, apologizing appropriately, discussing solutions, setting expectations, and closing professionally.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa20',
        'Recruiter Screening Call',
        'A first screening conversation between a recruiter and a job applicant.',
        'This roleplay is a realistic recruiter screening call before a full interview. The conversation should cover background, motivation, role fit, salary range, language skills, notice period, and next steps using professional spoken German.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa21',
        'Contract Review Discussion',
        'A business conversation about contract terms between a company representative and a partner or legal contact.',
        'This roleplay focuses on reviewing contract terms in German. The conversation should include timelines, payment conditions, liability, responsibilities, changes, approval steps, and careful clarification of wording.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa22',
        'Training Session',
        'An instructional conversation between a trainer and an employee learning a new process or tool.',
        'This roleplay happens during a workplace training session. The conversation should include explanations, process steps, examples, learner questions, practical clarifications, and confirmation of understanding in clear German.',
        false
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa23',
        'Office Conflict Mediation',
        'A sensitive workplace conversation between a manager or HR representative and an employee.',
        'This roleplay addresses interpersonal tension in a professional setting. The conversation should include describing the issue, listening, clarifying misunderstandings, proposing constructive solutions, setting boundaries, and maintaining respectful language.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa24',
        'Board Presentation Preparation',
        'A strategy-focused conversation between a presenter and a senior colleague or manager.',
        'This roleplay happens while preparing for an important executive presentation. The conversation should include structure, data points, key messages, likely questions, risks, recommendations, and concise business phrasing.',
        true
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa25',
        'Factory Safety Briefing',
        'A practical workplace conversation between a supervisor and a new worker on safety procedures.',
        'This roleplay takes place during a safety briefing in an industrial workplace. The conversation should include rules, protective equipment, emergency procedures, restricted areas, reporting problems, and checking understanding with clear language.',
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
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb601',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa6',
        'Team Member',
        'You are giving a short update in a team meeting. You explain what is finished, what is in progress, what problems exist, and what support you need.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb602',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa6',
        'Project Lead',
        'You lead the meeting. You ask for a clear update, clarify risks, check deadlines, and help define the next steps in a professional way.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb701',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa7',
        'Client',
        'You represent the client in a kickoff call. You explain your goals, ask questions about scope and timing, and clarify expectations for the project.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb702',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa7',
        'Consultant',
        'You represent the service provider. You lead the kickoff professionally, gather requirements, explain the process, and clarify deliverables and responsibilities.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb801',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa8',
        'Employee',
        'You are receiving a performance review. You reflect on your work, respond to feedback, discuss achievements and challenges, and talk about future goals.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb802',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa8',
        'Manager',
        'You are conducting the review. You give balanced feedback, discuss goals, ask reflective questions, and keep the conversation respectful and constructive.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb901',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa9',
        'Employee or Candidate',
        'You want to negotiate compensation professionally. You explain your reasons, mention achievements or qualifications, and respond carefully to offers or concerns.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb902',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa9',
        'Manager or Recruiter',
        'You are discussing compensation with the employee or candidate. You ask about expectations, explain company constraints, and negotiate in a calm professional tone.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1a1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa10',
        'Employee',
        'You have a technical problem that affects your work. You describe the issue, answer troubleshooting questions, and explain what you already tried.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1a2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa10',
        'IT Support Specialist',
        'You are internal IT support. You identify the issue, ask precise troubleshooting questions, suggest steps, and communicate clearly and efficiently.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1b1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa11',
        'Candidate',
        'You are following up after an interview. You ask about the timeline, clarify any open questions, and respond professionally to feedback or next steps.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1b2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa11',
        'Recruiter',
        'You speak with the candidate after the interview. You discuss impressions, process steps, scheduling, and any remaining practical questions professionally.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1c1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa12',
        'New Employee',
        'You are starting a new job. You introduce yourself, ask practical questions, and try to understand the team, tools, and expectations.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1c2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa12',
        'Team Lead',
        'You welcome the new employee. You explain routines, priorities, tools, people, and next steps in a supportive and organized way.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1d1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa13',
        'Potential Buyer',
        'You are evaluating a product for your company. You ask practical questions about features, pricing, implementation, and business value.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1d2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa13',
        'Sales Representative',
        'You are presenting the product. You explain features clearly, respond to objections, link benefits to business needs, and suggest logical next steps.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1e1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa14',
        'Project Manager',
        'You need to explain that a project deadline is at risk. You describe the situation, propose solutions, and manage expectations professionally.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1e2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa14',
        'Stakeholder',
        'You need an update on the project. You ask about the causes of delay, alternatives, risks, and the new timeline.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1f1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa15',
        'Conference Attendee',
        'You are networking at a professional event. You introduce yourself, explain your work, ask smart questions, and look for common professional interests.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb1f2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa15',
        'Industry Professional',
        'You meet someone at a conference. You describe your role, discuss industry topics, and respond openly to possible collaboration or networking follow-up.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2a1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa16',
        'Business Traveler',
        'You are checking into a hotel during a work trip. You confirm the booking, ask practical business-travel questions, and clarify any company-related details.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2a2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa16',
        'Hotel Receptionist',
        'You check in the guest, confirm details, explain hotel services, and answer practical questions clearly and politely.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2b1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa17',
        'Buyer',
        'You are negotiating with a supplier. You discuss pricing, delivery conditions, reliability, and quality expectations for your company.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2b2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa17',
        'Supplier Representative',
        'You represent the supplier. You explain pricing, respond to demands, discuss delivery and quality, and negotiate professionally.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2c1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa18',
        'Marketing Manager',
        'You are planning a campaign. You discuss target audience, channels, budget, priorities, and expected results in a structured way.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2c2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa18',
        'Marketing Specialist or Agency Contact',
        'You help design the campaign. You ask clarifying questions, suggest ideas, discuss timing and KPIs, and help turn goals into a concrete plan.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2d1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa19',
        'Customer',
        'You are unhappy about a product or service problem. You explain the issue, describe its impact, and ask for a fair and practical solution.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2d2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa19',
        'Customer Service Representative',
        'You handle the complaint professionally. You listen, clarify the issue, apologize appropriately, and work toward a realistic solution.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2e1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa20',
        'Applicant',
        'You are speaking with a recruiter for an initial screening. You present your background, motivation, availability, and salary expectations professionally.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2e2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa20',
        'Recruiter',
        'You conduct the screening call. You ask about experience, role fit, salary, language skills, and next steps in a structured professional tone.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2f1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa21',
        'Business Partner',
        'You want to review and clarify contract terms. You ask about obligations, deadlines, payments, and any risky or unclear wording.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb2f2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa21',
        'Company Representative',
        'You explain the contract terms and respond to questions carefully. You clarify wording, discuss conditions, and work toward agreement professionally.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3a1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa22',
        'Trainee',
        'You are learning a new process or system. You ask questions, repeat steps to confirm understanding, and seek practical examples.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3a2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa22',
        'Trainer',
        'You explain the new process step by step. You check understanding, answer questions, and adapt your explanations clearly.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3b1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa23',
        'Employee',
        'You are involved in a workplace conflict. You describe your concerns, explain what happened from your perspective, and discuss constructive solutions.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3b2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa23',
        'Manager or HR Representative',
        'You mediate a workplace conflict. You ask neutral questions, listen carefully, clarify misunderstandings, and try to move toward a professional resolution.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3c1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa24',
        'Presenter',
        'You are preparing for an important board or executive presentation. You explain your message, check your structure, and discuss likely questions.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3c2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa24',
        'Senior Colleague',
        'You help prepare the presenter. You challenge unclear points, ask likely executive questions, and help sharpen the message and recommendations.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3d1',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa25',
        'New Worker',
        'You are receiving a safety briefing in a factory or industrial workplace. You ask practical questions and confirm that you understand the procedures.'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbb3d2',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa25',
        'Supervisor',
        'You explain workplace safety rules, equipment, emergency procedures, and reporting responsibilities clearly and seriously.'
    )
ON CONFLICT (id) DO UPDATE
SET
    scenario_id = EXCLUDED.scenario_id,
    role_name = EXCLUDED.role_name,
    prompt_context = EXCLUDED.prompt_context;

COMMIT;
