/* ----- {{copyright}} --- */
// NGRX
import { createFeatureSelector, createSelector } from '@ngrx/store';
// Lodash
import { each } from 'lodash';
// CRUD
import { QueryResultsModel, HttpExtenstionsModel } from '@core/_base/crud';

// State
import { %class%State } from '../_reducers/{{selector}}.tab.reducers';
import { %class%Model } from '../_models/{{selector}}.tab.model';

export const select{{class}}State = createFeatureSelector<{{class}}State>('{{class}}');

export const selectProductSpecificationById = ({{class}}Id: number) => createSelector(
    select{{class}}State,
    {{class}}State => {{class}}State.entities[{{class}}Id]
);

export const select{{class}}PageLoading = createSelector(
    select{{class}}State,
    {{class}}State => {{class}}State.loading
);



export const selectLastCreated{{class}}Id = createSelector(
    select{{class}}State,
    {{class}}State => {{class}}State.lastCreated{{class}}Id
);


export const selectPSShowInitWaitingMessage = createSelector(
    select{{class}}State,
    {{class}}State => {{class}}State.showInitWaitingMessage
);




export const select{{class}}InStore = createSelector(
    select{{class}}State,
    {{class}}State => {
        const items: {{class}}Model[] = [];
        each({{class}}State.entities, element => {
            items.push(element);
        });
        const httpExtension = new HttpExtenstionsModel();
        const result: {{class}}Model[] = httpExtension.sortArray(items, {{class}}State.lastQuery.sortField, {{class}}State.lastQuery.sortOrder);
        return new QueryResultsModel(result, {{class}}State.totalCount, '');
    }
);

