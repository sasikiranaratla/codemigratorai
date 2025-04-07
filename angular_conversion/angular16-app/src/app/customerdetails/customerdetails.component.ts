
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CustomerDetails } from '../customerdetails';
import { DataService } from '../data.service';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-customerdetails',
  templateUrl: './customerdetails.component.html',
  styleUrls: ['./customerdetails.component.css'],
  standalone: true,
  imports: [CommonModule, RouterModule]
})
export class CustomerdetailsComponent implements OnInit {
  customerDetails: CustomerDetails | null = null;
  
  private dataService = inject(DataService);
  private activeRoute = inject(ActivatedRoute);
  private router = inject(Router);

  ngOnInit(): void {
    this.getCustomerDetails();
  }

  getCustomerDetails(): void {
    this.activeRoute.params.subscribe(routeParams => {
      this.dataService.getCustomerDetails(routeParams['id']).subscribe(
        (customerDetails: CustomerDetails) => {
          this.customerDetails = customerDetails;
          console.log(customerDetails);
        }
      );
    });
  }

  goToCustomerPage(): void {
    this.router.navigateByUrl("/customers");
  }
}
