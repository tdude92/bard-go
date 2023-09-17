//
//  AutoSoundTrackView.swift
//  AutoSoundtrack
//
//  Created by Matthews Ma on 2023-09-16.
//

import SwiftUI



struct AutoSoundTrackView: View {
    
//    @ObservedObject var cameraModel = CameraDataModel()
    @ObservedObject var viewModel = AutoSoundtrackViewModel(serverBaseURL: "https://autosoundtrack.ingridqin.repl.co")
    var body: some View {
        ZStack {
//            CameraView()
            Button("send req") {
                Task {
                    await viewModel.getEmotionVectorHTTP()
                }
            }
        }
    }
}

struct AutoSoundTrackView_Previews: PreviewProvider {
    static var previews: some View {
        AutoSoundTrackView()
    }
}
