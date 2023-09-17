//
//  AutoSoundtrackViewModel.swift
//  AutoSoundtrack
//
//  Created by Matthews Ma on 2023-09-16.
//

import Foundation
import SwiftUI
import os.log

class AutoSoundtrackViewModel: ObservableObject {
    @Published var viewfinderImage: Image?
    @Published var viewfinderCIImage: CIImage?
    @Published var thumbnailImage: Image?
    
    var isPhotosLoaded = false
    let camera = Camera()

    let serverBaseURL: String
    
    init(serverBaseURL: String) {
        self.serverBaseURL = serverBaseURL
        Task {
            await handleCameraPreviews()
        }
    }
    
    // camera stuff
    func handleCameraPreviews() async {
        let imageStream = camera.previewStream

        for await image in imageStream {
            Task { @MainActor in
                // convert to Image type
                viewfinderImage = image.image
                // keep as CIImage type
                viewfinderCIImage = image
            }
        }
    }
    
    // send to serverBaseURL and get back a mood
    func getEmotionVectorHTTP() async {
        guard let url = URL(string: "\(serverBaseURL)/api/image") else {
            return
        }
        // encode image in to send over post
        guard let encoded = try? JSONEncoder().encode(convertCIImageToBase64String(ciImage: viewfinderCIImage)) else {
            print("Failed to encode order")
            return
        }

        var request = URLRequest(url: url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpMethod = "POST"
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error)")
                return
            }

            if let data = data, let responseString = String(data: data, encoding: .utf8) {
                print("Response: \(responseString)")
            }
        }

        task.resume()
    }
}


func convertCIImageToBase64String(ciImage: CIImage?) -> String? {
    guard let a = ciImage else {
        return nil
    }
    let context = CIContext(options: nil)
    guard let cgImage = context.createCGImage(ciImage!, from: ciImage!.extent) else { return nil }
    
    let uiImage = UIImage(cgImage: cgImage)
    guard let pngData = uiImage.pngData() else { return nil }
    
    return pngData.base64EncodedString()
}

// camera stuff
fileprivate struct PhotoData {
    var thumbnailImage: Image
    var thumbnailSize: (width: Int, height: Int)
    var imageData: Data
    var imageSize: (width: Int, height: Int)
}

fileprivate extension CIImage {
    var image: Image? {
        let ciContext = CIContext()
        guard let cgImage = ciContext.createCGImage(self, from: self.extent) else { return nil }
        return Image(decorative: cgImage, scale: 1, orientation: .up)
    }
}

fileprivate extension Image.Orientation {

    init(_ cgImageOrientation: CGImagePropertyOrientation) {
        switch cgImageOrientation {
        case .up: self = .up
        case .upMirrored: self = .upMirrored
        case .down: self = .down
        case .downMirrored: self = .downMirrored
        case .left: self = .left
        case .leftMirrored: self = .leftMirrored
        case .right: self = .right
        case .rightMirrored: self = .rightMirrored
        }
    }
}

fileprivate let logger = Logger(subsystem: "ma.matthews.autosoundtrack", category: "DataModel")
