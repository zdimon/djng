/* -----  --- */
// NGRX
import { createFeatureSelector, createSelector } from '@ngrx/store';
// Lodash
import { each } from 'lodash';
// CRUD
import { QueryResultsModel, HttpExtenstionsModel } from '@core/_base/crud';
// State
import { ModerationsState } from '../_reducers/moderation.reducers';
import { ModerationModel } from '../_models/moderation.model';

export const selectModerationsState = createFeatureSelector<ModerationsState>('moderation');

export const selectModerationById = (moderationId: number) => createSelector(
    selectModerationsState,
    moderationsState => moderationsState.entities[moderationId]
);

export const selectModerationsPageLoading = createSelector(
    selectModerationsState,
    moderationsState => moderationsState.listLoading
);

export const selectModerationsActionLoading = createSelector(
    selectModerationsState,
    customersState => customersState.actionsloading
);

export const selectModerationsPageLastQuery = createSelector(
    selectModerationsState,
    moderationsState => moderationsState.lastQuery
);

export const selectLastCreatedModerationId = createSelector(
    selectModerationsState,
    moderationsState => moderationsState.lastCreatedModerationId
);

export const selectModerationsInitWaitingMessage = createSelector(
    selectModerationsState,
    moderationsState => moderationsState.showInitWaitingMessage
);

export const selectModerationsInStore = createSelector(
    selectModerationsState,
    moderationState => {
        const items: ModerationModel[] = [];
        each(moderationState.entities, element => {
            items.push(element);
        });
        const httpExtension = new HttpExtenstionsModel();
        const result: ModerationModel[] = httpExtension.sortArray(items, moderationState.lastQuery.sortField, moderationState.lastQuery.sortOrder);
        return new QueryResultsModel(result, moderationState.totalCount, '');
    }
);

export const selectHasModerationsInStore = createSelector(
    selectModerationsInStore,
    queryResult => {
        if (!queryResult.totalCount) {
            return false;
        }

        return true;
    }
);
