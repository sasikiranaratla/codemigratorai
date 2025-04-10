
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DataService } from '../data.service';
import { Customer } from '../customer';
import { Router } from '@angular/router';

@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.css'],
  standalone: true,
  imports: [CommonModule, RouterModule]
})
export class CustomersComponent implements OnInit {
  customers: Customer[] = [];
  selectedCustomer: string = "temp";
  
  constructor(private dataService: DataService, private router: Router) { }

  ngOnInit(): void {
    this.getCustomerList();
  }

  getCustomerList(): void {
    this.dataService.getCustomerList().subscribe({
      next: (customers: Customer[]) => {
        this.customers = customers;
        this.selectedCustomer = customers[0]?.name || '';
        console.log(customers);
      }
    });
  }

  setSelectedCustomer(cust: string): void {
    this.selectedCustomer = cust;
  }

  goToDetailsPage(id: number): void {
    this.router.navigateByUrl(`/customerdetails/${id}`);
  }
}
