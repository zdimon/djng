// NGRX
import { createFeatureSelector, createSelector } from '@ngrx/store';
// Lodash
import { each } from 'lodash';
// CRUD
import { HttpExtenstionsModel, QueryResultsModel } from '../../../_base/crud';
import { VideoModel } from '../_models/video.model';
// State
import { VideosState } from '../_reducers/video.reducers';

export const selectVideosState = createFeatureSelector<VideosState>('videos');

export const selectVideoById = (videoId: number) => createSelector(
    selectVideosState,
    videosState => videosState.entities[videoId],
);

export const selectVideosPageLoading = createSelector(
    selectVideosState,
    videosState => videosState.listLoading,
);

export const selectVideosActionLoading = createSelector(
    selectVideosState,
    customersState => customersState.actionsloading,
);

export const selectVideosPageLastQuery = createSelector(
    selectVideosState,
    videosState => videosState.lastQuery,
);

export const selectLastCreatedVideoId = createSelector(
    selectVideosState,
    videosState => videosState.lastCreatedVideoId,
);

export const selectVideosInitWaitingMessage = createSelector(
    selectVideosState,
    videosState => videosState.showInitWaitingMessage,
);

export const selectVideosInStore = createSelector(
    selectVideosState,
    videosState => {
        const items: VideoModel[] = [];
        each(videosState.entities, element => {
            items.push(element);
        });
        const httpExtension = new HttpExtenstionsModel();
        const result: VideoModel[] = httpExtension.sortArray(items, videosState.lastQuery.sortField, videosState.lastQuery.sortOrder);
        return new QueryResultsModel(result, videosState.totalCount, '');
    },
);

export const selectHasVideosInStore = createSelector(
    selectVideosInStore,
    queryResult => {
        if (!queryResult.totalCount) {
            return false;
        }

        return true;
    },
);
