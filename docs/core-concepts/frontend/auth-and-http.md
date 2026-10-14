# Auth and HTTP

### Google Login

The app uses the Google Identity Services authorization code flow. `index.html` loads `https://accounts.google.com/gsi/client`, and `GoogleAuthService` (`src/app/shared/services/google-auth.service.ts`) creates a code client with `google.accounts.oauth2.initCodeClient`, using `environment.googleOauthClientId`, scope `email profile`, and `environment.googleOauthCallbackUrl` as the redirect URI.

1. **Open the popup:** the login button calls `loginWithGoogle()`, which calls `codeClient.requestCode()`.
2. **Exchange the code:** Google returns a code, and the service posts `{ code }` to `authentication/google/login/` with `withCredentials: true`.
3. **Set cookies:** the backend verifies the code and sets the JWT cookies on the response. The frontend never sees the tokens.
4. **Load the user:** `LoginComponent` dispatches `getAuthUser()` and `getMeUser()`, then navigates to the `returnUrl` query param if it is a safe in-app path, otherwise `/dashboard`.

If the returned user has `is_active === false`, the component calls logout, resets the session, and shows a deactivated account message instead.

### Backend Endpoints

`LoginService` (`src/app/views/authentication/services/login.service.ts`) and `UserMgmtService` cover the rest:

| Endpoint                        | Called by                         | Purpose                                  |
| ------------------------------- | --------------------------------- | ---------------------------------------- |
| `authentication/google/login/`  | `GoogleAuthService`               | Exchange the Google code for cookies     |
| `authentication/user/`          | `LoginService.getAuthUser()`      | Fetch the auth user                      |
| `authentication/token/verify/`  | `LoginService.postVerifyUser()`   | Check the access cookie (used by guards) |
| `authentication/token/refresh/` | `LoginService`, `authInterceptor` | Refresh the access cookie                |
| `authentication/logout/`        | `LoginService.postLogout()`       | Clear the cookies                        |
| `api/users/me/`                 | `UserMgmtService.getMeUser()`     | Current user with roles and memberships  |

### JWT Cookies

The backend sets the tokens as HttpOnly cookies named `access` and `refresh` (`JWT_AUTH_COOKIE` and `JWT_AUTH_REFRESH_COOKIE` in `config/settings/base.py`). JavaScript cannot read them, so nothing token related is stored in localStorage. The browser only sends them when a request has `withCredentials: true`.

### Interceptors

Interceptors are registered in `app.config.ts` and run in this order:

1. **`authInterceptor`** (`shared/services/auth-interceptor.service.ts`): skips any URL that does not start with `environment.apiURL`. For API requests it sets `withCredentials: true`. On a `401` from anything other than `token/refresh`, `token/verify`, `logout`, or `auth/login`, it posts to `${environment.apiURL}authentication/token/refresh/` and retries the original request. Concurrent `401`s wait on the same refresh. If the refresh fails, it navigates to `/auth/login` with `returnUrl` set to the current page.
2. **`csrfInterceptor`** (`shared/services/auth-csrf-interceptor.service.ts`): also limited to `environment.apiURL`. It reads the `csrftoken` cookie from `document.cookie` and sends it as the `X-CSRFToken` header.
3. **`loaderInterceptor`** (`shared/interceptors/loader.interceptor.ts`): shows the global loader for each request and hides it in `finalize`. It skips requests whose URL contains an entry in `SILENT_URLS` (for example `token/verify`, `users/me`, `notifications/unread-count`, notebook status calls) or that set the `SKIP_GLOBAL_LOADER` context token.

```typescript
this.http.get(url, {
  context: new HttpContext().set(SKIP_GLOBAL_LOADER, true),
});
```

**Important:** credentials and the CSRF header are scoped to `environment.apiURL` on purpose. Third party calls, such as the GitHub search used by the Pipelines page, reject credentialed CORS requests and custom headers.

### The `me` User and Role Gates

`api/users/me/` returns the current user with `is_platform_admin`, `is_data_analyst`, `permissions.groups`, `lab_memberships`, `project_memberships`, and `requires_aup_acknowledgment`. It is stored in the `user-management` slice as `getMeUser` and read through `UserMgmtFacade`.

| Accessor                                | Use it for                                                      |
| --------------------------------------- | --------------------------------------------------------------- |
| `getMeUserSignal` / `getMeUser$`        | Display. May be a rehydrated copy from localStorage             |
| `getCurrentUserSignal` / `currentUser$` | Authorization. Only set once `/me` has answered in this session |

Guards always use `currentUser$`. UI role checks go through `deriveUserRoles()` and `effectiveUserRoles()` in `src/app/shared/utils/user-roles.ts`, which turn the user into flags like `isPlatformAdmin`, `isDataAnalyst`, `isLabDirector`, `isBioinformaticsUser`, `isLabCollaborator`, and `isLabScopedUser`. A platform admin who switches into one of their own labs takes on that lab membership's roles.

`me` is refetched on login, by the guards when no current user exists, and by `LayoutContainerComponent` whenever the route path changes. When `/me` returns a different user ID than `SessionOwnerService` has stored, an effect in `user-mgmt.effects.ts` dispatches a session reset and then puts the new user back.

**Important:** role gates read the cached `me` user. If an action changes the signed in user's own roles, dispatch `getMeUser()` afterwards or the UI keeps showing the old permissions until the next route change.

### Environments

Each file in `src/environments` exports an `IAppEnvironment` (`environment.model.ts`):

| Field                    | Meaning                                                      |
| ------------------------ | ------------------------------------------------------------ |
| `apiURL`                 | Backend base URL, with a trailing slash                      |
| `googleOauthClientId`    | Google OAuth client ID                                       |
| `googleOauthCallbackUrl` | Redirect URI registered with Google, ending in `/auth/login` |

`angular.json` swaps `environment.ts` for the right file with `fileReplacements`:

| Configuration | File                         | `apiURL`                             |
| ------------- | ---------------------------- | ------------------------------------ |
| `local`       | `environment.local.ts`       | `http://localhost:8000/`             |
| `development` | `environment.development.ts` | `https://api.apgap.dev.rtd.asu.edu/` |
| `uat`         | `environment.uat.ts`         | `https://api.apgap.uat.rtd.asu.edu/` |
| `production`  | `environment.production.ts`  | `https://api.apgap.azpathogens.org/` |

`ng serve` defaults to `local` and `ng build` defaults to `production`. `environment.template.ts` holds `${apgap_host_url}` placeholders for a commented out `envsubst` step in Cloud Build and is not used by any configuration.
