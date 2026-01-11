"""
Google Sheets Integration for BloodConnect

This module handles synchronization of application data to Google Sheets.
"""

import os
import logging
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings

logger = logging.getLogger(__name__)

class GoogleSheetsClient:
    """Client for Google Sheets API operations."""
    
    def __init__(self):
        self.spreadsheet_id = settings.GOOGLE_SHEETS_SPREADSHEET_ID
        self.credentials_path = settings.GOOGLE_SHEETS_CREDENTIALS_PATH
        self.service = None
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                self.service = build('sheets', 'v4', credentials=credentials)
                logger.info("Google Sheets client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google Sheets client: {e}")
        else:
            logger.warning("Google Sheets credentials not found. Integration disabled.")
    
    def append_row(self, sheet_name, values):
        """
        Append a row to the specified sheet.
        
        Args:
            sheet_name (str): Name of the sheet (e.g., 'BloodBanks')
            values (list): List of values to append
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.service:
            logger.warning("Google Sheets service not available")
            return False
        
        try:
            range_name = f"{sheet_name}!A:A"  # Append to first column
            
            # Prepare the request body
            body = {
                'values': [values]
            }
            
            # Execute the append request
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Successfully appended row to {sheet_name}")
            return True
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error appending to Google Sheets: {e}")
            return False
    
    def update_blood_bank(self, blood_bank):
        """Sync blood bank data to Google Sheets."""
        values = [
            str(blood_bank.id),
            blood_bank.username,
            blood_bank.name,
            blood_bank.city,
            blood_bank.address,
            blood_bank.phone,
            blood_bank.email or '',
            str(blood_bank.latitude),
            str(blood_bank.longitude),
            'Verified' if blood_bank.is_verified else 'Pending',
            blood_bank.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ]
        
        return self.append_row(settings.GOOGLE_SHEETS['BLOOD_BANKS'], values)
    
    def update_donor(self, donor):
        """Sync donor data to Google Sheets."""
        values = [
            str(donor.id),
            donor.name,
            donor.blood_group,
            donor.phone,
            donor.city,
            donor.email or '',
            donor.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ]
        
        return self.append_row(settings.GOOGLE_SHEETS['DONORS'], values)
    
    def update_sos_request(self, sos_request):
        """Sync SOS request data to Google Sheets."""
        values = [
            str(sos_request.id),
            sos_request.requester_name,
            sos_request.blood_group,
            sos_request.city,
            sos_request.phone,
            sos_request.hospital_name or '',
            sos_request.address or '',
            sos_request.urgency_notes or '',
            'Active' if sos_request.is_active else 'Inactive',
            sos_request.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ]
        
        return self.append_row(settings.GOOGLE_SHEETS['SOS_REQUESTS'], values)
    
    def update_blood_stock(self, blood_stock):
        """Sync blood stock data to Google Sheets."""
        values = [
            str(blood_stock.id),
            blood_stock.blood_bank.name,
            blood_stock.blood_bank.city,
            blood_stock.blood_group,
            str(blood_stock.quantity),
            str(blood_stock.price_per_unit),
            'Available' if blood_stock.is_available else 'Not Available',
            blood_stock.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        ]
        
        return self.append_row(settings.GOOGLE_SHEETS['BLOOD_STOCK'], values)


# Global client instance
sheets_client = GoogleSheetsClient()


def sync_blood_bank_to_sheets(blood_bank):
    """Sync blood bank registration to Google Sheets."""
    return sheets_client.update_blood_bank(blood_bank)


def sync_donor_to_sheets(donor):
    """Sync donor registration to Google Sheets."""
    return sheets_client.update_donor(donor)


def sync_sos_request_to_sheets(sos_request):
    """Sync SOS request to Google Sheets."""
    return sheets_client.update_sos_request(sos_request)


def sync_blood_stock_to_sheets(blood_stock):
    """Sync blood stock update to Google Sheets."""
    return sheets_client.update_blood_stock(blood_stock)
