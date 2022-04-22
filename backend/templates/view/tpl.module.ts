/* ----- {{copyright}} --- */
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
    {{ camelName }}Reducer,
    {{ upname }}Effects,
    {{ upname }}Service
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
import { %upname%Component } from './{{fileprefix}}.component';

/// Tabs

{% for tab in tabs %}
import { {{tab.class}}TabListComponent } from './tabs/list/{{tab.selector}}.component';
import { {{tab.class}}Effects } from './../store/_effects/{{tab.selector}}.tab.effects';
import { {{tab.class}}Reducer } from './../store/_reducers/{{tab.selector}}.tab.reducers';
import { {{tab.class}}Service } from './../store/_services/{{tab.selector}}.tab.services';
{% endfor %}

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

import {%upname%ListComponent} from './list/{{fileprefix}}-list.component';
import {%upname%EditComponent} from './edit/{{fileprefix}}-edit.component';
// tslint:disable-next-line:class-name
const routes: Routes = [
    {
        path: '',
        component: {{upname}}Component,
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
                component: {{upname}}ListComponent
            },
            {
                path: 'edit',
                component: {{upname}}EditComponent
            },
            {
                path: 'add',
                component: {{upname}}EditComponent
            },
            {
                path: 'edit/:id',
                component: {{upname}}EditComponent
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
        StoreModule.forFeature('{{camelName}}', {{camelName}}Reducer),
        EffectsModule.forFeature([{{upname}}Effects]),
        {% for tab in tabs %}
        StoreModule.forFeature('{{tab.class}}', {{tab.class}}Reducer),
        EffectsModule.forFeature([{{tab.class}}Effects]),
        {% endfor %}
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
        {{upname}}Service,
        {% for tab in tabs %}
        {{tab.class}}Service,
        {% endfor %}
    ],
    entryComponents: [
        ActionNotificationComponent,
        DeleteEntityDialogComponent,
        FetchEntityDialogComponent,
        UpdateStatusDialogComponent
    ],
    declarations: [
        {{upname}}Component,
        {{upname}}ListComponent,
        {{upname}}EditComponent,
        {% for tab in tabs %}
        {{tab.class}}TabListComponent,
        {% endfor %}
    ]
})
export class {{ upname }}Module { }
