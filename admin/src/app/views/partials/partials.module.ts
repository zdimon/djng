// Angular
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
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
    MatTooltipModule,
} from '@angular/material';
import { RouterModule } from '@angular/router';
// NgBootstrap
import {NgbDropdownModule, NgbTabsetModule, NgbTooltipModule} from '@ng-bootstrap/ng-bootstrap';
// SVG inline
import {InlineSVGModule} from 'ng-inline-svg';
// Perfect Scrollbar
import {PerfectScrollbarModule} from 'ngx-perfect-scrollbar';
// Core module
import {CoreModule} from '../../core/core.module';
// CRUD Partials
import {
    ActionNotificationComponent,
    AlertComponent,
    DeleteEntityDialogComponent,
    FetchEntityDialogComponent,
    UpdateStatusDialogComponent,
} from './content/crud';
// Errpr
import {ErrorComponent} from './content/general/error/error.component';
// General
import {NoticeComponent} from './content/general/notice/notice.component';
import {PortletModule} from './content/general/portlet/portlet.module';
// Extra module
import {WidgetModule} from './content/widgets/widget.module';
// Layout partials
import {
    ContextMenu2Component,
    ContextMenuComponent,
    LanguageSelectorComponent,
    NotificationComponent,
    QuickActionComponent,
    QuickPanelComponent,
    ScrollTopComponent,
    SearchDefaultComponent,
    SearchDropdownComponent,
    SearchResultComponent,
    SplashScreenComponent,
    StickyToolbarComponent,
    SubheaderSearchComponent,
    UserProfileComponent,
} from './layout';
import {CartComponent} from './layout/topbar/cart/cart.component';

@NgModule({
    declarations: [
        ScrollTopComponent,
        NoticeComponent,
        ActionNotificationComponent,
        DeleteEntityDialogComponent,
        FetchEntityDialogComponent,
        UpdateStatusDialogComponent,
        AlertComponent,

        // topbar components
        ContextMenu2Component,
        ContextMenuComponent,
        QuickPanelComponent,
        ScrollTopComponent,
        SearchResultComponent,
        SplashScreenComponent,
        StickyToolbarComponent,
        SubheaderSearchComponent,
        LanguageSelectorComponent,
        NotificationComponent,
        QuickActionComponent,
        SearchDefaultComponent,
        SearchDropdownComponent,
        UserProfileComponent,
        CartComponent,

        ErrorComponent,
    ],
    exports: [
        WidgetModule,
        PortletModule,

        ScrollTopComponent,
        NoticeComponent,
        ActionNotificationComponent,
        DeleteEntityDialogComponent,
        FetchEntityDialogComponent,
        UpdateStatusDialogComponent,
        AlertComponent,

        // topbar components
        ContextMenu2Component,
        ContextMenuComponent,
        QuickPanelComponent,
        ScrollTopComponent,
        SearchResultComponent,
        SplashScreenComponent,
        StickyToolbarComponent,
        SubheaderSearchComponent,
        LanguageSelectorComponent,
        NotificationComponent,
        QuickActionComponent,
        SearchDefaultComponent,
        SearchDropdownComponent,
        UserProfileComponent,
        CartComponent,

        ErrorComponent,
    ],
    imports: [
        CommonModule,
        RouterModule,
        FormsModule,
        ReactiveFormsModule,
        PerfectScrollbarModule,
        InlineSVGModule,
        CoreModule,
        PortletModule,
        WidgetModule,

        // angular material modules
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
        MatDialogModule,

        // ng-bootstrap modules
        NgbDropdownModule,
        NgbTabsetModule,
        NgbTooltipModule,
    ],
})
export class PartialsModule {
}
