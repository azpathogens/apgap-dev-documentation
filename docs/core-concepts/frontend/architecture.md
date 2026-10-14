# Architecture

### Bootstrap

`src/main.ts` calls `bootstrapApplication(AppComponent, appConfig)`. There are no NgModules. Everything is registered as providers in `src/app/app.config.ts`:

| Provider                                                                     | What it does                                                        |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `provideStore({}, { metaReducers: [resetStateOnSessionChange] })`            | Empty root store. Feature slices register themselves later          |
| `provideEffects([])`                                                         | Root effects runner. Features add their own effects                 |
| `provideStoreDevtools({ maxAge: 25 })`                                       | Redux DevTools, keeping the last 25 actions                         |
| `provideZoneChangeDetection({ eventCoalescing: true })`                      | Zone based change detection                                         |
| `provideAppInitializer(() => inject(ThemeService).init())`                   | Applies the light or dark theme before first render                 |
| `provideRouter(routes, withRouterConfig({ onSameUrlNavigation: 'reload' }))` | Root routes from `app.routes.ts`                                    |
| `...sharedConfig`, `...labsConfig`, and the other feature configs            | Feature state, effects, and routes                                  |
| `provideHttpClient(withInterceptors([...]))`                                 | `authInterceptor`, `csrfInterceptor`, `loaderInterceptor`, in order |

### Session Reset

`resetStateOnSessionChange` (`src/app/shared/state/meta-reducers/reset-state.meta-reducer.ts`) is a root meta-reducer. When it sees `[Session] Reset Session State`, it rebuilds the whole store from `undefined`, so every slice goes back to its initial state. The only thing carried across is `shared.themeState`, because the theme is a device preference.

Dispatch the reset through `SessionFacade.resetSessionState()`. The app does this on logout, on landing at the login page, when the OAuth callback fails, and when `/me` returns a different user than the one stored by `SessionOwnerService`.

### Feature Config Pattern

Each feature with state exports an array of providers from a `*.config.ts` file, which `app.config.ts` spreads in. `src/app/views/labs/lab.config.ts` is a typical one:

```typescript
const localStorageSyncReducer = createLocalStorageSyncReducer<LabsState>([
  "labList",
  "getLabDetail",
  "getLabProjectUsersList",
  "selectedLab",
]);

export const labsConfig = [
  provideState(labsStateKey, LabsReducer, {
    metaReducers: [localStorageSyncReducer],
  }),
  provideState(uploadsStateKey, UploadsReducer),
  provideState(sequenceMetadataStateKey, SequenceMetadataReducer),
  provideRouter(LabsRoutes),
  provideEffects([LabsEffects, UploadsEffects, SequenceMetadataEffects]),
];
```

Features without NgRx state, such as `aup-report` or `pathogens`, have no config file. They only export a `*.routing.ts` that `app.routes.ts` lazy loads.

### Inside a Feature

```text
views/labs/
  lab.config.ts          providers (state, effects, routes)
  lab.routing.ts         LabsRoutes
  lab-registration.ts    side nav menu entry
  components/            presentational and page components
  containers/            smart components that wire facades to components
  facade/                LabFacade and friends
  modals/                dialogs
  models/                TypeScript interfaces
  services/              HTTP calls through ApiService
  state/
    index.ts             state keys and feature selectors
    actions/             *-ui.actions.ts and *-api.actions.ts
    effects/             call services, dispatch API success or failure
    reducers/            createReducer with an initialState
    selectors/           createSelector over the feature slice
```

The flow is: a component calls a facade method, the facade dispatches a UI action, an effect calls the service and dispatches an API action, the reducer stores the result, and the facade exposes it through a selector.

### Facade Pattern

Components never inject `Store` directly. They use a facade that is `providedIn: 'root'`. From `src/app/views/labs/facade/lab.facade.ts`:

```typescript
@Injectable({ providedIn: "root" })
export class LabFacade {
  private readonly store = inject(Store<LabsState>);

  getLabList$ = this.store.select(labSelectors.getLabList);
  labListSignal: Signal<ILab[]> = toSignal(this.getLabList$, {
    initialValue: [],
  });

  public getLabs() {
    this.store.dispatch(LabsActions.LabsUiActions.GetLabs());
  }
}
```

Each piece of state is exposed both as an Observable (`$` suffix) and as a Signal. Templates usually read the Signal.

### Shared State

`src/app/shared/shared.config.ts` registers one feature key, `shared` (`sharedStateKey` in `src/app/shared/state/index.ts`), holding these slices: `navigationState`, `organizationState`, `analyticalDatasetRequestState`, `fileState`, `archiveRequestState`, `loaderState`, and `themeState`. Each slice lives in its own folder under `src/app/shared/state` with actions, reducers, selectors, facades, and effects where needed. `state/session` has no slice. It only holds the reset action and `SessionFacade`.

### Persisted State

`createLocalStorageSyncReducer` (`src/app/shared/utils/local-storage-sync.ts`) wraps `ngrx-store-localstorage` with `rehydrate: true` and `removeOnUndefined: true`. It also seeds each slice with its `initialState` and stops rehydrating after a session reset.

| Feature            | Persisted keys                                                                                                          |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `shared`           | `navigationState.sideNavMenuItems`, `organizationState.organizationList`, `themeState.theme`, `themeState.userOverride` |
| `authentication`   | `user`                                                                                                                  |
| `user-management`  | `selectedUser`, `getUserList`, `getMeUser`                                                                              |
| `labs`             | `labList`, `getLabDetail`, `getLabProjectUsersList`, `selectedLab`                                                      |
| `projects`         | `projectsList`, `selectedProject`, `projectDetails`, `projectUsersList`, `projectPermissionGroups`                      |
| `datasets`         | `selectDataset`                                                                                                         |
| `notifications`    | `notifications`                                                                                                         |
| `metadata-mgmt`    | `metadataMgmt`                                                                                                          |
| `metadata-tags`    | `metadataTags`                                                                                                          |
| `domain-allowlist` | `domainAllowlist`                                                                                                       |

**Important:** the login page wipes localStorage on every visit (`clearSessionStorage()` keeps only the `apgap-theme` key). Anything that must survive a new login belongs on the server, not in persisted state.

### Menu Registration

The side nav is built from registration classes that implement `IModuleRegistration` (`src/app/shared/module-registration.ts/base.registration.ts`): a `title`, a `breadcrumb`, `getPermissions()`, and `getMenu()` returning `IMenuItem[]`. Examples are `views/labs/lab-registration.ts` and `views/admin-settings/admin-settings.registration.ts`.

`NavigationService.getAllMenuItems()` (`src/app/shared/services/navigation.service.ts`) lists the registrations in order and filters them by role. Platform admins get Administration, Data Analysts get only Dashboard, Datasets, Reporting, and Catalog Overview, and lab scoped users get a separate menu from `buildLabScopedMenu()`.

### Adding a New Feature

1. **Create the folder:** add `src/app/views/<feature>/` with `components/`, `models/`, and `services/`. Add `state/` and `facade/` if the feature keeps state.
2. **Write the service:** inject `ApiService` and build URLs with `buildFullURL('api/<resource>', '...')`.
3. **Add state:** define UI and API actions, an effect that calls the service, a reducer with an `initialState`, a state key and selectors in `state/index.ts`.
4. **Add a facade:** `providedIn: 'root'`, exposing selectors as Observables and Signals and one method per action.
5. **Add routes:** export `<Feature>Routes` from `<feature>.routing.ts`.
6. **Add a config:** export `<feature>Config` with `provideState`, `provideEffects`, and `provideRouter`, and spread it into `app.config.ts`. Only add a localStorage sync reducer if the data is safe to show from a stale cache.
7. **Register the route:** add a `loadChildren` entry under the layout route in `app.routes.ts` with a breadcrumb.
8. **Add a menu entry:** create a registration class, or add a link to an existing one, and include it in `NavigationService` with the right role filter.
