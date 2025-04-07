
// app.component.ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [RouterOutlet]
})
export class AppComponent {
  title = 'app';
}

// customers.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class CustomersComponent {
  // Component logic
}

// customerdetails.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-customerdetails',
  templateUrl: './customerdetails.component.html',
  styleUrls: ['./customerdetails.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class CustomerdetailsComponent {
  // Component logic
}

// display.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class DisplayComponent {
  // Component logic
}

// app-routing.module.ts
import { Routes } from '@angular/router';
import { CustomersComponent } from './customers/customers.component';
import { CustomerdetailsComponent } from './customerdetails/customerdetails.component';
import { DisplayComponent } from './display/display.component';

export const routes: Routes = [
  { path: 'customers', component: CustomersComponent },
  { path: 'customerdetails', component: CustomerdetailsComponent },
  { path: 'display', component: DisplayComponent },
  { path: '', redirectTo: '/customers', pathMatch: 'full' }
];

// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { AppComponent } from './app/app.component';
import { routes } from './app/app-routing.module';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    provideRouter(routes)
  ]
});
