
// Angular
import { OverlayModule } from '@angular/cdk/overlay';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { APP_INITIALIZER, NgModule } from '@angular/core';
import { GestureConfig, MatProgressSpinnerModule } from '@angular/material';
import { BrowserModule, HAMMER_GESTURE_CONFIG } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { EffectsModule } from '@ngrx/effects';
import { StoreRouterConnectingModule } from '@ngrx/router-store';
// NGRX
import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { TranslateModule } from '@ngx-translate/core';
// Angular in memory
import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
// Hammer JS
import 'hammerjs';
import * as json from 'highlight.js/lib/languages/json';
import * as scss from 'highlight.js/lib/languages/scss';
import * as typescript from 'highlight.js/lib/languages/typescript';
import * as xml from 'highlight.js/lib/languages/xml';
// SVG inline
import { InlineSVGModule } from 'ng-inline-svg';
// Highlight JS
import { HIGHLIGHT_OPTIONS, HighlightLanguage } from 'ngx-highlightjs';
// Perfect Scroll bar
import { PERFECT_SCROLLBAR_CONFIG, PerfectScrollbarConfigInterface } from 'ngx-perfect-scrollbar';
// NGX Permissions
import { NgxPermissionsModule } from 'ngx-permissions';
// Env
import { environment } from '../environments/environment';
// Modules
import { AppRoutingModule } from './app-routing.module';
// Copmponents
import { AppComponent } from './app.component';
// CRUD
import { HttpUtilsService, LayoutUtilsService, TypesUtilsService } from './core/_base/crud';
// Layout Services
import {
    DataTableService,
    // FakeApiService,
    KtDialogService,
    LayoutConfigService,
    LayoutRefService,
    MenuAsideService,
    MenuConfigService,
    MenuHorizontalService,
    PageConfigService,
    SplashScreenService,
    SubheaderService,
} from './core/_base/layout';
// Config
import { LayoutConfig } from './core/_config/layout.config';
import { AuthService } from './core/auth';
import { CoreModule } from './core/core.module';
// State
import { metaReducers, reducers } from './core/reducers';
// Auth
import { AuthModule } from './views/pages/auth/auth.module';
// Partials
import { PartialsModule } from './views/partials/partials.module';
import { ThemeModule } from './views/theme/theme.module';

import { AuthInterceptor } from './core/auth.interseptor';
import { SessionService } from './core/session.service';

// tslint:disable-next-line:class-name
const DEFAULT_PERFECT_SCROLLBAR_CONFIG: PerfectScrollbarConfigInterface = {
    wheelSpeed: 0.5,
    swipeEasing: true,
    minScrollbarLength: 40,
    maxScrollbarLength: 300,
};

export function initializeLayoutConfig(appConfig: LayoutConfigService) {
    // initialize app by loading default demo layout config
    return () => {
        if (appConfig.getConfig() === null) {
            appConfig.loadConfigs(new LayoutConfig().configs);
        }
    };
}

export function hljsLanguages(): HighlightLanguage[] {
    return [
        {name: 'typescript', func: typescript},
        {name: 'scss', func: scss},
        {name: 'xml', func: xml},
        {name: 'json', func: json},
    ];
}

// @ts-ignore
@NgModule({
    declarations: [AppComponent],
    imports: [
        BrowserAnimationsModule,
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        // environment.isMockEnabled ? HttpClientInMemoryWebApiModule.forRoot(FakeApiService, {
        //     passThruUnknownUrl: true,
        //     dataEncapsulation: false
        // }) : [],
        NgxPermissionsModule.forRoot(),
        PartialsModule,
        CoreModule,
        OverlayModule,
        StoreModule.forRoot(reducers, {metaReducers}),
        EffectsModule.forRoot([]),
        StoreRouterConnectingModule.forRoot({stateKey: 'router'}),
        StoreDevtoolsModule.instrument(),
        AuthModule.forRoot(),
        TranslateModule.forRoot(),
        MatProgressSpinnerModule,
        InlineSVGModule.forRoot(),
        ThemeModule,
    ],
    exports: [],
    providers: [
        AuthService,
        LayoutConfigService,
        LayoutRefService,
        MenuConfigService,
        PageConfigService,
        KtDialogService,
        DataTableService,
        SplashScreenService,
        {
            provide: PERFECT_SCROLLBAR_CONFIG,
            useValue: DEFAULT_PERFECT_SCROLLBAR_CONFIG,
        },
        {
            provide: HAMMER_GESTURE_CONFIG,
            useClass: GestureConfig,
        },
        {
            // layout config initializer
            provide: APP_INITIALIZER,
            useFactory: initializeLayoutConfig,
            deps: [LayoutConfigService], multi: true,
        },
        {
            provide: HIGHLIGHT_OPTIONS,
            useValue: {languages: hljsLanguages},
        },
        // template services
        SubheaderService,
        MenuHorizontalService,
        MenuAsideService,
        HttpUtilsService,
        TypesUtilsService,
        LayoutUtilsService,
        { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
        SessionService,
    ],
    bootstrap: [AppComponent],
})
export class AppModule {
}
