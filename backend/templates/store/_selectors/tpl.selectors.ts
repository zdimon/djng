/* ----- {{copyright}} --- */
// NGRX
import { createFeatureSelector, createSelector } from '@ngrx/store';
// Lodash
import { each } from 'lodash';
// CRUD
import { QueryResultsModel, HttpExtenstionsModel } from '@core/_base/crud';
// State
import { %upname%sState } from '../_reducers/{{fileprefix}}.reducers';
import { %upname%Model } from '../_models/{{fileprefix}}.model';

export const select{{upname}}sState = createFeatureSelector<{{upname}}sState>('{{camelName}}');

export const select{{upname}}ById = ({{camelName}}Id: number) => createSelector(
    select{{upname}}sState,
    {{camelName}}sState => {{camelName}}sState.entities[{{camelName}}Id]
);

export const select{{upname}}sPageLoading = createSelector(
    select{{upname}}sState,
    {{camelName}}sState => {{camelName}}sState.listLoading
);

export const select{{upname}}sActionLoading = createSelector(
    select{{upname}}sState,
    customersState => customersState.actionsloading
);

export const select{{upname}}sPageLastQuery = createSelector(
    select{{upname}}sState,
    {{camelName}}sState => {{camelName}}sState.lastQuery
);

export const selectLastCreated{{upname}}Id = createSelector(
    select{{upname}}sState,
    {{camelName}}sState => {{camelName}}sState.lastCreated{{upname}}Id
);

export const select{{upname}}sInitWaitingMessage = createSelector(
    select{{upname}}sState,
    {{camelName}}sState => {{camelName}}sState.showInitWaitingMessage
);

export const select{{upname}}sInStore = createSelector(
    select{{upname}}sState,
    {{camelName}}State => {
        const items: {{upname}}Model[] = [];
        each({{camelName}}State.entities, element => {
            items.push(element);
        });
        const httpExtension = new HttpExtenstionsModel();
        const result: {{upname}}Model[] = httpExtension.sortArray(items, {{camelName}}State.lastQuery.sortField, {{camelName}}State.lastQuery.sortOrder);
        return new QueryResultsModel(result, {{camelName}}State.totalCount, '');
    }
);

export const selectHas{{upname}}sInStore = createSelector(
    select{{upname}}sInStore,
    queryResult => {
        if (!queryResult.totalCount) {
            return false;
        }

        return true;
    }
);
