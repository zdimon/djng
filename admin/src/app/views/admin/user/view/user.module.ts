/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
// Angular
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

// Translate Module
import { TranslateModule } from '@ngx-translate/core';
// NGRX
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
// UI
import { PartialsModule } from '../../../partials/partials.module';

// Auth
import { ModuleGuard } from '@core/auth';
import { AuthInterceptor } from '@core/auth.interseptor';
// Core => Services
import {
    userReducer,
    UserEffects,
    UserService
} from '../store';
// Core => Utils
import {
    TypesUtilsService,
    InterceptService,
    LayoutUtilsService,
} from '@core/_base/crud';

import { HttpUtilsService } from '../store';

// Shared
import {
    ActionNotificationComponent,
    DeleteEntityDialogComponent,
    FetchEntityDialogComponent,
    UpdateStatusDialogComponent
} from '../../../partials/content/crud';
// Components
import { UserComponent } from './user.component';

/// Tabs


import { UserMediaTabListComponent } from './tabs/list/user-media-list.component';
import { UserMediaEffects } from './../store/_effects/user-media-list.tab.effects';
import { UserMediaReducer } from './../store/_reducers/user-media-list.tab.reducers';
import { UserMediaService } from './../store/_services/user-media-list.tab.services';


// Date format issue

import {MomentModule} from "ngx-moment";
import {MomentDateAdapter} from '@angular/material-moment-adapter';
import {DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE} from "@angular/material";
export const ISO_FORMAT = {
   parse: {
       dateInput: 'LL',
   },
   display: {
       dateInput: 'YYYY-MM-DD',
       monthYearLabel: 'MMM YYYY',
       dateA11yLabel: 'LL',
       monthYearA11yLabel: 'MMMM YYYY',
   },
};


// Material
import {
    MAT_DIALOG_DEFAULT_OPTIONS,
    MatAutocompleteModule,
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatDialogModule,
    MatIconModule,
    MatInputModule,
    MatMenuModule,
    MatNativeDateModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatSelectModule,
    MatSnackBarModule,
    MatSortModule,
    MatTableModule,
    MatTabsModule,
    MatTooltipModule
} from '@angular/material';
import { NgbProgressbarModule } from '@ng-bootstrap/ng-bootstrap';
import { NgxPermissionsModule } from 'ngx-permissions';
import {SharedModule} from "@base/layout/shared/shared.module";

import {UserListComponent} from './list/user-list.component';
import {UserEditComponent} from './edit/user-edit.component';
// tslint:disable-next-line:class-name
const routes: Routes = [
    {
        path: '',
        component: UserComponent,
        // canActivate: [ModuleGuard],
        // data: { moduleName: 'ecommerce' },
        children: [
            {
                path: '',
                redirectTo: 'list',
                pathMatch: 'full'
            },
            {
                path: 'list',
                component: UserListComponent
            },
            {
                path: 'edit',
                component: UserEditComponent
            },
            {
                path: 'add',
                component: UserEditComponent
            },
            {
                path: 'edit/:id',
                component: UserEditComponent
            }
        ]
    }
];

@NgModule({
    imports: [
        MatDialogModule,
        CommonModule,
        HttpClientModule,
        PartialsModule,
        NgxPermissionsModule.forChild(),
        RouterModule.forChild(routes),
        FormsModule,
        ReactiveFormsModule,
        TranslateModule.forChild(),
        MatButtonModule,
        MatMenuModule,
        MatSelectModule,
        MatInputModule,
        MatTableModule,
        MatAutocompleteModule,
        MatRadioModule,
        MatIconModule,
        MatNativeDateModule,
        MatProgressBarModule,
        MatDatepickerModule,
        MatCardModule,
        MatPaginatorModule,
        MatSortModule,
        MatCheckboxModule,
        MatProgressSpinnerModule,
        MatSnackBarModule,
        MatTabsModule,
        MatTooltipModule,
        NgbProgressbarModule,
        StoreModule.forFeature('user', userReducer),
        EffectsModule.forFeature([UserEffects]),
        
        StoreModule.forFeature('UserMedia', UserMediaReducer),
        EffectsModule.forFeature([UserMediaEffects]),
        
		SharedModule
	],
    providers: [
        ModuleGuard,
        AuthInterceptor,
        {
            provide: HTTP_INTERCEPTORS,
            useClass: AuthInterceptor,
            multi: true
        },
        {
            provide: MAT_DIALOG_DEFAULT_OPTIONS,
            useValue: {
                hasBackdrop: true,
                panelClass: 'kt-mat-dialog-container__wrapper',
                height: 'auto',
                width: '900px'
            }
        },
        TypesUtilsService,
        LayoutUtilsService,
        HttpUtilsService,
        TypesUtilsService,
        LayoutUtilsService,
        UserService,
        
        UserMediaService,
        
    ],
    entryComponents: [
        ActionNotificationComponent,
        DeleteEntityDialogComponent,
        FetchEntityDialogComponent,
        UpdateStatusDialogComponent
    ],
    declarations: [
        UserComponent,
        UserListComponent,
        UserEditComponent,
        
        UserMediaTabListComponent,
        
    ]
})
export class UserModule { }