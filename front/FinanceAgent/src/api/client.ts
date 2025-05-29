import { makeApi, Zodios, type ZodiosOptions } from "@zodios/core";
import { z } from "zod";

const MonthTracking = z.object({ text: z.string() }).passthrough();
const SenderEnum = z.enum(["user", "agent"]);
const Message = z
  .object({
    id: z.number().int(),
    conversation: z.number().int(),
    sender: SenderEnum,
    content_type: z.string().max(20),
    payload: z.any(),
    timestamp: z.string().datetime({ offset: true }),
    status: z.string().max(20),
  })
  .passthrough();
const ChatSendRequest = z.object({ text: z.string() }).passthrough();
const CredentialTypes = z
  .object({
    key: z.string(),
    name: z.string(),
    fields: z.array(z.object({}).partial().passthrough()),
  })
  .passthrough();
const TagGoal = z
  .object({
    id: z.number().int(),
    value: z.number(),
    user: z.number().int().nullish(),
    tag: z.number().int().nullish(),
  })
  .passthrough();
const User = z
  .object({
    id: z.number().int(),
    password: z.string().max(128),
    last_login: z.string().datetime({ offset: true }).nullish(),
    is_superuser: z.boolean().optional(),
    username: z
      .string()
      .max(150)
      .regex(/^[\w.@+-]+$/),
    first_name: z.string().max(150).optional(),
    last_name: z.string().max(150).optional(),
    email: z.string().max(254).email().optional(),
    is_staff: z.boolean().optional(),
    is_active: z.boolean().optional(),
    date_joined: z.string().datetime({ offset: true }).optional(),
    groups: z.array(z.number().int()).optional(),
    user_permissions: z.array(z.number().int()).optional(),
  })
  .passthrough();
const BankInfo = z.object({ key: z.string(), value: z.number() }).passthrough();
const Login = z
  .object({
    username: z.string().optional(),
    email: z.string().email().optional(),
    password: z.string(),
  })
  .passthrough();
const Token = z.object({ key: z.string().max(40) }).passthrough();
const RestAuthDetail = z.object({ detail: z.string() }).passthrough();
const PasswordChange = z
  .object({
    new_password1: z.string().max(128),
    new_password2: z.string().max(128),
  })
  .passthrough();
const PasswordReset = z.object({ email: z.string().email() }).passthrough();
const PasswordResetConfirm = z
  .object({
    new_password1: z.string().max(128),
    new_password2: z.string().max(128),
    uid: z.string(),
    token: z.string(),
  })
  .passthrough();
const Register = z
  .object({
    username: z.string().min(1).max(150).optional(),
    email: z.string().email(),
    password1: z.string(),
    password2: z.string(),
  })
  .passthrough();
const ResendEmailVerification = z
  .object({ email: z.string().email() })
  .passthrough();
const VerifyEmail = z.object({ key: z.string() }).passthrough();
const UserDetails = z
  .object({
    pk: z.number().int(),
    username: z
      .string()
      .max(150)
      .regex(/^[\w.@+-]+$/),
    email: z.string().email(),
    first_name: z.string().max(150).optional(),
    last_name: z.string().max(150).optional(),
  })
  .passthrough();
const PatchedUserDetails = z
  .object({
    pk: z.number().int(),
    username: z
      .string()
      .max(150)
      .regex(/^[\w.@+-]+$/),
    email: z.string().email(),
    first_name: z.string().max(150),
    last_name: z.string().max(150),
  })
  .partial()
  .passthrough();
const MonthCategory = z
  .object({
    category_id: z.number().int(),
    category: z.string(),
    key: z.string(),
    value: z.number(),
    goal: z.number().int(),
    type: z.string(),
    percent: z.number(),
    color: z.string(),
  })
  .passthrough();
const SummeryWidgets = z
  .object({
    graphs: z.object({}).partial().passthrough(),
    average_expenses: z.number(),
    average_income: z.number(),
    number_of_months: z.number().int(),
    average_bank_expenses: z.number(),
  })
  .passthrough();
const TotalMonthExpenses = z
  .object({
    moving_average: z.number(),
    value: z.number(),
    text: z.string(),
    color: z.string(),
  })
  .passthrough();
const Credential = z
  .object({
    id: z.number().int(),
    company: z.string(),
    type: z.string(),
    last_scanned: z.string().nullish(),
    additional_info: z.unknown().optional(),
    balance: z.string(),
  })
  .passthrough();
const PatchedCredential = z
  .object({
    id: z.number().int(),
    company: z.string(),
    type: z.string(),
    last_scanned: z.string().nullable(),
    additional_info: z.unknown(),
    balance: z.string(),
  })
  .partial()
  .passthrough();
const RecurringTransaction = z
  .object({
    id: z.number().int(),
    name: z.string().max(200),
    date: z.string(),
    value: z.number(),
    user: z.number().int().nullish(),
    credential: z.number().int().nullish(),
  })
  .passthrough();
const PatchedRecurringTransaction = z
  .object({
    id: z.number().int(),
    name: z.string().max(200),
    date: z.string(),
    value: z.number(),
    user: z.number().int().nullable(),
    credential: z.number().int().nullable(),
  })
  .partial()
  .passthrough();
const TypeEnum = z.enum(["MONTHLY FIXED", "PERIODIC", "CONTINUOUS"]);
const Tag = z
  .object({
    id: z.number().int(),
    key: z.string().max(128).nullish(),
    name: z.string().max(128),
    expense: z.boolean().optional(),
    type: TypeEnum.optional(),
    user: z.number().int().nullish(),
  })
  .passthrough();
const PatchedTag = z
  .object({
    id: z.number().int(),
    key: z.string().max(128).nullable(),
    name: z.string().max(128),
    expense: z.boolean(),
    type: TypeEnum,
    user: z.number().int().nullable(),
  })
  .partial()
  .passthrough();
const TransactionRest = z
  .object({
    id: z.number().int(),
    tag_name: z.string(),
    date: z.string(),
    name: z.string().max(200),
    value: z.number(),
    month: z.number().int().gte(-2147483648).lte(2147483647).nullish(),
    month_date: z.string().nullish(),
    bank: z.boolean().optional(),
    identifier: z.string().max(64).nullish(),
    user: z.number().int().nullish(),
    credential: z.number().int().nullish(),
    tag: z.number().int().nullish(),
  })
  .passthrough();
const PatchedTransactionRest = z
  .object({
    id: z.number().int(),
    tag_name: z.string(),
    date: z.string(),
    name: z.string().max(200),
    value: z.number(),
    month: z.number().int().gte(-2147483648).lte(2147483647).nullable(),
    month_date: z.string().nullable(),
    bank: z.boolean(),
    identifier: z.string().max(64).nullable(),
    user: z.number().int().nullable(),
    credential: z.number().int().nullable(),
    tag: z.number().int().nullable(),
  })
  .partial()
  .passthrough();
const UserTransactionsNames = z.object({ name: z.string() }).passthrough();

export const schemas = {
  MonthTracking,
  SenderEnum,
  Message,
  ChatSendRequest,
  CredentialTypes,
  TagGoal,
  User,
  BankInfo,
  Login,
  Token,
  RestAuthDetail,
  PasswordChange,
  PasswordReset,
  PasswordResetConfirm,
  Register,
  ResendEmailVerification,
  VerifyEmail,
  UserDetails,
  PatchedUserDetails,
  MonthCategory,
  SummeryWidgets,
  TotalMonthExpenses,
  Credential,
  PatchedCredential,
  RecurringTransaction,
  PatchedRecurringTransaction,
  TypeEnum,
  Tag,
  PatchedTag,
  TransactionRest,
  PatchedTransactionRest,
  UserTransactionsNames,
};

const endpoints = makeApi([
  {
    method: "get",
    path: "/api/chat/history/",
    alias: "api_chat_history_retrieve",
    requestFormat: "json",
    response: z.array(Message),
  },
  {
    method: "post",
    path: "/api/chat/send/",
    alias: "api_chat_send_create",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: ChatSendRequest,
      },
    ],
    response: Message,
  },
  {
    method: "get",
    path: "/api/month-tracking",
    alias: "api_month_tracking_retrieve",
    requestFormat: "json",
    response: z.object({ text: z.string() }).passthrough(),
  },
  {
    method: "get",
    path: "/api/user_credentials/",
    alias: "api_user_credentials_retrieve",
    requestFormat: "json",
    response: CredentialTypes,
  },
  {
    method: "post",
    path: "/api/user_credentials/",
    alias: "api_user_credentials_create",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: CredentialTypes,
      },
    ],
    response: CredentialTypes,
  },
  {
    method: "post",
    path: "/api/user_goals/",
    alias: "api_user_goals_create",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: TagGoal,
      },
    ],
    response: TagGoal,
  },
  {
    method: "get",
    path: "/api/users/",
    alias: "api_users_retrieve",
    requestFormat: "json",
    response: User,
  },
  {
    method: "get",
    path: "/bank_info.*",
    alias: "bank_info.*_retrieve",
    requestFormat: "json",
    response: BankInfo,
  },
  {
    method: "post",
    path: "/dj-rest-auth/login/",
    alias: "dj_rest_auth_login_create",
    description: `Check the credentials and return the REST Token
if the credentials are valid and authenticated.
Calls Django Auth login method to register User ID
in Django session framework

Accept the following POST parameters: username, password
Return the REST Framework Token Object&#x27;s key.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: Login,
      },
    ],
    response: z.object({ key: z.string().max(40) }).passthrough(),
  },
  {
    method: "post",
    path: "/dj-rest-auth/logout/",
    alias: "dj_rest_auth_logout_create",
    description: `Calls Django logout method and delete the Token object
assigned to the current User object.

Accepts/Returns nothing.`,
    requestFormat: "json",
    response: z.object({ detail: z.string() }).passthrough(),
  },
  {
    method: "post",
    path: "/dj-rest-auth/password/change/",
    alias: "dj_rest_auth_password_change_create",
    description: `Calls Django Auth SetPasswordForm save method.

Accepts the following POST parameters: new_password1, new_password2
Returns the success/fail message.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: PasswordChange,
      },
    ],
    response: z.object({ detail: z.string() }).passthrough(),
  },
  {
    method: "post",
    path: "/dj-rest-auth/password/reset/",
    alias: "dj_rest_auth_password_reset_create",
    description: `Calls Django Auth PasswordResetForm save method.

Accepts the following POST parameters: email
Returns the success/fail message.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: z.object({ email: z.string().email() }).passthrough(),
      },
    ],
    response: z.object({ detail: z.string() }).passthrough(),
  },
  {
    method: "post",
    path: "/dj-rest-auth/password/reset/confirm/",
    alias: "dj_rest_auth_password_reset_confirm_create",
    description: `Password reset e-mail link is confirmed, therefore
this resets the user&#x27;s password.

Accepts the following POST parameters: token, uid,
    new_password1, new_password2
Returns the success/fail message.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: PasswordResetConfirm,
      },
    ],
    response: z.object({ detail: z.string() }).passthrough(),
  },
  {
    method: "post",
    path: "/dj-rest-auth/registration/",
    alias: "dj_rest_auth_registration_create",
    description: `Registers a new user.

Accepts the following POST parameters: username, email, password1, password2.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: Register,
      },
    ],
    response: z.object({ key: z.string().max(40) }).passthrough(),
  },
  {
    method: "post",
    path: "/dj-rest-auth/registration/resend-email/",
    alias: "dj_rest_auth_registration_resend_email_create",
    description: `Resends another email to an unverified email.

Accepts the following POST parameter: email.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: z.object({ email: z.string().email() }).passthrough(),
      },
    ],
    response: z.object({ detail: z.string() }).passthrough(),
  },
  {
    method: "post",
    path: "/dj-rest-auth/registration/verify-email/",
    alias: "dj_rest_auth_registration_verify_email_create",
    description: `Verifies the email associated with the provided key.

Accepts the following POST parameter: key.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: z.object({ key: z.string() }).passthrough(),
      },
    ],
    response: z.object({ detail: z.string() }).passthrough(),
  },
  {
    method: "get",
    path: "/dj-rest-auth/user/",
    alias: "dj_rest_auth_user_retrieve",
    description: `Reads and updates UserModel fields
Accepts GET, PUT, PATCH methods.

Default accepted fields: username, first_name, last_name
Default display fields: pk, username, email, first_name, last_name
Read-only fields: pk, email

Returns UserModel fields.`,
    requestFormat: "json",
    response: UserDetails,
  },
  {
    method: "put",
    path: "/dj-rest-auth/user/",
    alias: "dj_rest_auth_user_update",
    description: `Reads and updates UserModel fields
Accepts GET, PUT, PATCH methods.

Default accepted fields: username, first_name, last_name
Default display fields: pk, username, email, first_name, last_name
Read-only fields: pk, email

Returns UserModel fields.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: UserDetails,
      },
    ],
    response: UserDetails,
  },
  {
    method: "patch",
    path: "/dj-rest-auth/user/",
    alias: "dj_rest_auth_user_partial_update",
    description: `Reads and updates UserModel fields
Accepts GET, PUT, PATCH methods.

Default accepted fields: username, first_name, last_name
Default display fields: pk, username, email, first_name, last_name
Read-only fields: pk, email

Returns UserModel fields.`,
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: PatchedUserDetails,
      },
    ],
    response: UserDetails,
  },
  {
    method: "get",
    path: "/month_category.*",
    alias: "month_category.*_retrieve",
    requestFormat: "json",
    response: MonthCategory,
  },
  {
    method: "get",
    path: "/summery_widgets.*",
    alias: "summery_widgets.*_retrieve",
    requestFormat: "json",
    response: SummeryWidgets,
  },
  {
    method: "get",
    path: "/total_month_expenses.*",
    alias: "total_month_expenses.*_retrieve",
    requestFormat: "json",
    response: TotalMonthExpenses,
  },
  {
    method: "get",
    path: "/user_accounts/",
    alias: "user_accounts_list",
    requestFormat: "json",
    response: z.array(Credential),
  },
  {
    method: "post",
    path: "/user_accounts/",
    alias: "user_accounts_create",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: Credential,
      },
    ],
    response: Credential,
  },
  {
    method: "get",
    path: "/user_accounts/:id/",
    alias: "user_accounts_retrieve",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: Credential,
  },
  {
    method: "put",
    path: "/user_accounts/:id/",
    alias: "user_accounts_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: Credential,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: Credential,
  },
  {
    method: "patch",
    path: "/user_accounts/:id/",
    alias: "user_accounts_partial_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: PatchedCredential,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: Credential,
  },
  {
    method: "delete",
    path: "/user_accounts/:id/",
    alias: "user_accounts_destroy",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: z.void(),
  },
  {
    method: "get",
    path: "/user_recurring_transactions/",
    alias: "user_recurring_transactions_list",
    requestFormat: "json",
    response: z.array(RecurringTransaction),
  },
  {
    method: "post",
    path: "/user_recurring_transactions/",
    alias: "user_recurring_transactions_create",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: RecurringTransaction,
      },
    ],
    response: RecurringTransaction,
  },
  {
    method: "get",
    path: "/user_recurring_transactions/:id/",
    alias: "user_recurring_transactions_retrieve",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: RecurringTransaction,
  },
  {
    method: "put",
    path: "/user_recurring_transactions/:id/",
    alias: "user_recurring_transactions_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: RecurringTransaction,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: RecurringTransaction,
  },
  {
    method: "patch",
    path: "/user_recurring_transactions/:id/",
    alias: "user_recurring_transactions_partial_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: PatchedRecurringTransaction,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: RecurringTransaction,
  },
  {
    method: "delete",
    path: "/user_recurring_transactions/:id/",
    alias: "user_recurring_transactions_destroy",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: z.void(),
  },
  {
    method: "get",
    path: "/user_tags/",
    alias: "user_tags_list",
    requestFormat: "json",
    response: z.array(Tag),
  },
  {
    method: "post",
    path: "/user_tags/",
    alias: "user_tags_create",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: Tag,
      },
    ],
    response: Tag,
  },
  {
    method: "get",
    path: "/user_tags/:id/",
    alias: "user_tags_retrieve",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: Tag,
  },
  {
    method: "put",
    path: "/user_tags/:id/",
    alias: "user_tags_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: Tag,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: Tag,
  },
  {
    method: "patch",
    path: "/user_tags/:id/",
    alias: "user_tags_partial_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: PatchedTag,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: Tag,
  },
  {
    method: "delete",
    path: "/user_tags/:id/",
    alias: "user_tags_destroy",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: z.void(),
  },
  {
    method: "get",
    path: "/user_transactions_names",
    alias: "user_transactions_names_retrieve",
    requestFormat: "json",
    response: z.object({ name: z.string() }).passthrough(),
  },
  {
    method: "get",
    path: "/user_transactions/",
    alias: "user_transactions_list",
    requestFormat: "json",
    parameters: [
      {
        name: "date",
        type: "Query",
        schema: z.string().optional(),
      },
      {
        name: "date__gt",
        type: "Query",
        schema: z.string().optional(),
      },
      {
        name: "date__gte",
        type: "Query",
        schema: z.string().optional(),
      },
      {
        name: "date__lt",
        type: "Query",
        schema: z.string().optional(),
      },
      {
        name: "date__lte",
        type: "Query",
        schema: z.string().optional(),
      },
    ],
    response: z.array(TransactionRest),
  },
  {
    method: "post",
    path: "/user_transactions/",
    alias: "user_transactions_create",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: TransactionRest,
      },
    ],
    response: TransactionRest,
  },
  {
    method: "get",
    path: "/user_transactions/:id/",
    alias: "user_transactions_retrieve",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: TransactionRest,
  },
  {
    method: "put",
    path: "/user_transactions/:id/",
    alias: "user_transactions_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: TransactionRest,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: TransactionRest,
  },
  {
    method: "patch",
    path: "/user_transactions/:id/",
    alias: "user_transactions_partial_update",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: PatchedTransactionRest,
      },
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: TransactionRest,
  },
  {
    method: "delete",
    path: "/user_transactions/:id/",
    alias: "user_transactions_destroy",
    requestFormat: "json",
    parameters: [
      {
        name: "id",
        type: "Path",
        schema: z.number().int(),
      },
    ],
    response: z.void(),
  },
]);

export const api = new Zodios(endpoints);

export function createApiClient(baseUrl: string, options?: ZodiosOptions) {
  return new Zodios(baseUrl, endpoints, options);
}
