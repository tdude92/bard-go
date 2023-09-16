//
//  AutoSoundtrackViewModel.swift
//  AutoSoundtrack
//
//  Created by Matthews Ma on 2023-09-16.
//

import Foundation
import SwiftUI

class AutoSoundtrackViewModel: ObservableObject {
    @Binding var viewFinderImageBinding: CIImage?
    let serverBaseURL: String
    
    init(viewFinderImageBinding: Binding<CIImage?>, serverBaseURL: String) {
        self._viewFinderImageBinding = viewFinderImageBinding
        self.serverBaseURL = serverBaseURL
    }
    
    func getEmotionVectorHTTP() async {
        guard let url = URL(string: "\(serverBaseURL)/imagetoemotion") else {
            return
        }
        // encode image in to send over post
        guard let encoded = try? JSONEncoder().encode(convertCIImageToBase64String(ciImage: viewFinderImageBinding!)) else {
            print("Failed to encode order")
            return
        }

        var request = URLRequest(url: url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        
        do {
            let (data, _) = try await URLSession.shared.upload(for: request, from: encoded)
            print("it worked?")
        } catch {
            print("Checkout failed.")
        }
    }
}


func convertCIImageToBase64String(ciImage: CIImage) -> String? {
    let context = CIContext(options: nil)
    guard let cgImage = context.createCGImage(ciImage, from: ciImage.extent) else { return nil }
    
    let uiImage = UIImage(cgImage: cgImage)
    guard let pngData = uiImage.pngData() else { return nil }
    
    return pngData.base64EncodedString()
}
