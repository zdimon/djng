/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
import { BaseModel } from '@core/_base/crud';


export class UserModel extends BaseModel {
    
        
            id: number;
        
    
        
            email: string;
        
    
        
            username: string;
        
    
        
            is_superuser: string;
        
    
        
            is_staff: string;
        
    
        
            is_active: string;
        
    

    clear() {
        
            
                
                
                    this.id = 0 ;
                
            
         
            
                
                    this.email = '' ;
                
                
            
         
            
                
                    this.username = '' ;
                
                
            
         
            
                
                    this.is_superuser = '' ;
                
                
            
         
            
                
                    this.is_staff = '' ;
                
                
            
         
            
                
                    this.is_active = '' ;
                
                
            
         
    }
}
