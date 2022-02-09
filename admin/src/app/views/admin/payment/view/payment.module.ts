/* -----  --- */
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
    paymentReducer,
    PaymentEffects,
    PaymentService
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
import { PaymentComponent } from './payment.component';

/// Tabs



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

import {PaymentListComponent} from './list/payment-list.component';
import {PaymentEditComponent} from './edit/payment-edit.component';
// tslint:disable-next-line:class-name
const routes: Routes = [
    {
        path: '',
        component: PaymentComponent,
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
                component: PaymentListComponent
            },
            {
                path: 'edit',
                component: PaymentEditComponent
            },
            {
                path: 'add',
                component: PaymentEditComponent
            },
            {
                path: 'edit/:id',
                component: PaymentEditComponent
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
        StoreModule.forFeature('payment', paymentReducer),
        EffectsModule.forFeature([PaymentEffects]),
        
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
        PaymentService,
        
    ],
    entryComponents: [
        ActionNotificationComponent,
        DeleteEntityDialogComponent,
        FetchEntityDialogComponent,
        UpdateStatusDialogComponent
    ],
    declarations: [
        PaymentComponent,
        PaymentListComponent,
        PaymentEditComponent,
        
    ]
})
export class PaymentModule { }