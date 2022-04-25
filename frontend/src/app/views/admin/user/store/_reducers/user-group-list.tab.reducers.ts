/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
// NGRX
import { createFeatureSelector } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter, Update } from '@ngrx/entity';
// Actions
import { UserGroupActions, UserGroupActionTypes } from '../_actions/user-group-list.tab.actions';
// Models
import { UserGroupModel } from '../_models/user-group-list.tab.model';
import { QueryParamsModel } from '@core/_base/crud';

export interface UserGroupState extends EntityState<UserGroupModel> {
    results: any;
    UserGroupId: number;
    loading: boolean;
    totalCount: number;
    lastCreatedUserGroupId: number;
    lastQuery: QueryParamsModel;
    showInitWaitingMessage: boolean;
}

export const adapter: EntityAdapter<UserGroupModel> = createEntityAdapter<UserGroupModel>();

export const initialUserGroupState: UserGroupState = adapter.getInitialState({
    loading: false,
    results: [],
    totalCount: 0,
    UserGroupId: undefined,
    lastCreatedUserGroupId: undefined,
    lastQuery: new QueryParamsModel({}),
    showInitWaitingMessage: true
});

export function UserGroupReducer(state = initialUserGroupState, action: UserGroupActions): UserGroupState {
    switch  (action.type) {
        case UserGroupActionTypes.UserGroupPageToggleLoading:
            return {
                ...state,
                loading: action.payload.isLoading,
                lastCreatedUserGroupId: undefined
            };
        case UserGroupActionTypes.UserGroupOnServerCreated:
            return {...state, loading: true};
        case UserGroupActionTypes.UserGroupCreated:
            return adapter.addOne(action.payload.UserGroup, {
                ...state,
                lastCreatedUserGroupId: action.payload.UserGroup.id
            });
        case UserGroupActionTypes.UserGroupUpdated:
            return adapter.updateOne(action.payload.partialUserGroup, state);
        case UserGroupActionTypes.OneUserGroupDeleted:
            return adapter.removeOne(action.payload.id, state);
        case UserGroupActionTypes.ManyUserGroupDeleted:
            return adapter.removeMany(action.payload.ids, state);
        case UserGroupActionTypes.UserGroupPageCancelled:
            return { ...state, totalCount: 0, loading: false, UserGroupId: undefined, lastQuery: new QueryParamsModel({})  };
        case UserGroupActionTypes.UserGroupPageRequested:
            return { ...state, totalCount: 0, loading: true, UserGroupId: action.payload.UserGroupId, lastQuery: action.payload.page };
        case UserGroupActionTypes.UserGroupPageLoaded:
            return adapter.addMany(action.payload.results, {
                ...initialUserGroupState,
                totalCount: action.payload.totalCount,
                loading: false,
                UserGroupId: state.UserGroupId,
                lastQuery: state.lastQuery,
                showInitWaitingMessage: false
            });
        default:
            return state;
    }
}

export const getUserGroupRemarlState = createFeatureSelector<UserGroupModel>('UserGroup');

export const {
    selectAll,
    selectEntities,
    selectIds,
    selectTotal
} = adapter.getSelectors();
