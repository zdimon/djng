/* ----- {{copyright}} --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { {{class}}Actions, {{class}}ActionTypes } from '../_actions/{{selector}}.tab.actions';
// Models
import { {{class}}Model } from '../_models/{{selector}}.tab.model';
import { QueryParamsModel } from '@core/_base/crud';

export interface {{class}}State extends EntityState<{{class}}Model> {
    results: any;
    {{class}}Id: number;
    loading: boolean;
    totalCount: number;
    lastCreated{{class}}Id: number;
    lastQuery: QueryParamsModel;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<{{class}}Model> = createEntityAdapter<{{class}}Model>();

export const initial{{class}}State: {{class}}State = adapter.getInitialState({
    loading: false,
    results: [],
    totalCount: 0,
    {{class}}Id: undefined,
    lastCreated{{class}}Id: undefined,
    lastQuery: new QueryParamsModel({}),
    showInitWaitingMessage: true
});

export function {{class}}Reducer(state = initial{{class}}State, action: {{class}}Actions): {{class}}State {
    switch  (action.type) {
        case {{class}}ActionTypes.{{class}}PageToggleLoading:
            return {
                ...state,
                loading: action.payload.isLoading,
                lastCreated{{class}}Id: undefined
            };
        case {{class}}ActionTypes.{{class}}OnServerCreated:
            return {...state, loading: true};
        case {{class}}ActionTypes.{{class}}Created:
            return adapter.addOne(action.payload.{{class}}, {
                ...state,
                lastCreated{{class}}Id: action.payload.{{class}}.id
            });
        case {{class}}ActionTypes.{{class}}Updated:
            return adapter.updateOne(action.payload.partial{{class}}, state);
        case {{class}}ActionTypes.One{{class}}Deleted:
            return adapter.removeOne(action.payload.id, state);
        case {{class}}ActionTypes.Many{{class}}Deleted:
            return adapter.removeMany(action.payload.ids, state);
        case {{class}}ActionTypes.{{class}}PageCancelled:
            return { ...state, totalCount: 0, loading: false, {{class}}Id: undefined, lastQuery: new QueryParamsModel({})  };
        case {{class}}ActionTypes.{{class}}PageRequested:
            return { ...state, totalCount: 0, loading: true, {{class}}Id: action.payload.{{class}}Id, lastQuery: action.payload.page };
        case {{class}}ActionTypes.{{class}}PageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initial{{class}}State,
                totalCount: action.payload.totalCount,
                loading: false,
                {{class}}Id: state.{{class}}Id,
                lastQuery: state.lastQuery,
                showInitWaitingMessage: false
            });
        default:
            return state;
    }
}

export const get{{class}}RemarlState = createFeatureSelector<{{class}}Model>('{{class}}');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
